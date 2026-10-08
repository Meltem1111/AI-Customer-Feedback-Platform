from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from analyzer import SentimentAnalyzer
from pydantic import BaseModel, Field, ValidationError
from typing import Literal
from sqlalchemy.orm import Session
from database import get_db
from models import Feedback
import json
from sqlalchemy import func

app = FastAPI(
    title="AI Customer Feedback API",
    description="Customer feedback sentiment analysis using Gemini",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

try:
    analyzer = SentimentAnalyzer()
    print("AI Servisi başarıyla yüklendi")
except Exception as ex:
    analyzer = None
    print(f"Hata: {ex}")

class AnalyzerRequest(BaseModel):
    text: str

class AnalysisResult(BaseModel):
    sentiment: Literal["Pozitif", "Negatif", "Nötr"]
    score: int = Field(ge=0, le=100)
    summary: str = Field(
        min_length=1
    )

    keywords: list[str] = Field(
        min_length=5,
        max_length=5
    )

    language: str = Field(
        min_length=1
    )

    category: Literal[
        "Restoran/Yemek",
        "Ürün",
        "Kargo/Teslimat",
        "Hizmet",
        "Diğer"
    ]
class FeedbackResponse(BaseModel):
    id: int
    text: str
    sentiment: Literal["Pozitif", "Negatif", "Nötr"]
    score: int = Field(ge=0, le=100)
    summary: str | None
    keywords: list[str]
    language: str | None
    category: str | None
    created_at: str | None

class PaginatedFeedbackResponse(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int
    items: list[FeedbackResponse]
    
class FeedbackStatsResponse(BaseModel):
    positive: int
    negative: int
    neutral: int
    average_score: float

@app.get("/")
def home():
    return {"message": "AI Customer Feedback API çalışıyor. Dokümantasyon için /docs adresine gidin."
    }
@app.get("/feedbacks", response_model=PaginatedFeedbackResponse)
def get_feedbacks(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    sentiment: Literal["Pozitif", "Negatif", "Nötr"] | None = Query(default=None),
    category: Literal[
        "Restoran/Yemek",
        "Ürün",
        "Kargo/Teslimat",
        "Hizmet",
        "Diğer"
    ] | None = Query(default=None),
    min_score: int | None = Query(default=None, ge=0, le=100),
    max_score: int | None = Query(default=None, ge=0, le=100),
    search: str | None = Query(default=None),
    sort_by: Literal["score", "created_at"] = Query(default="created_at"),
    sort_order: Literal["asc", "desc"] = Query(default="desc"),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * page_size

    query = db.query(Feedback)
    if min_score is not None and max_score is not None:
        if min_score > max_score:
            raise HTTPException(
                status_code=400,
                detail="min_score, max_score değerinden büyük olamaz."
            )
        
    if sentiment:
        query = query.filter(Feedback.sentiment == sentiment)

    if category:
        query = query.filter(Feedback.category == category)

    if min_score is not None:
        query = query.filter(Feedback.score >= min_score)

    if max_score is not None:
        query = query.filter(Feedback.score <= max_score)

    if search:
        query = query.filter(
            Feedback.text.contains(search))
    
    total = query.count()

    if sort_by == "score":
        sort_column = Feedback.score
    else:
        sort_column = Feedback.created_at

    if sort_order == "desc":
        sort_column = sort_column.desc()
    else:
        sort_column = sort_column.asc()

    feedbacks = (
        query
        .order_by(sort_column)
        .offset(offset)
        .limit(page_size)
        .all()
    )

    items = [
        FeedbackResponse(
            id=feedback.id,
            text=feedback.text,
            sentiment=feedback.sentiment,
            score=feedback.score,
            summary=feedback.summary,
            keywords=json.loads(feedback.keywords),
            language=feedback.language,
            category=feedback.category,
            created_at=feedback.created_at.isoformat()
                if feedback.created_at
                else None
        )
        for feedback in feedbacks
    ]

    total_pages = (total + page_size - 1) // page_size

    return PaginatedFeedbackResponse(
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
        items=items
    )
@app.get("/feedbacks/stats", response_model=FeedbackStatsResponse)
def get_feedback_stats(
    db: Session = Depends(get_db)
):
    positive = db.query(Feedback).filter(
        Feedback.sentiment == "Pozitif"
    ).count()

    negative = db.query(Feedback).filter(
        Feedback.sentiment == "Negatif"
    ).count()

    neutral = db.query(Feedback).filter(
        Feedback.sentiment == "Nötr"
    ).count()

    average_score = db.query(
        func.avg(Feedback.score)
    ).scalar()

    return FeedbackStatsResponse(
        positive=positive,
        negative=negative,
        neutral=neutral,
        average_score=round(float(average_score or 0), 1)
    )
@app.post("/analyze")
def analyze(
    request: AnalyzerRequest,
    db: Session = Depends(get_db)
): 
    if analyzer is None:
        raise HTTPException(
            status_code=500,
            detail="AI servisi başlatılamadı."
        )

    cleaned = validate_input(request.text)

    result = analyzer.analyze_text(cleaned)
    try:
        validated_result = AnalysisResult.model_validate(result)
    except ValidationError as ex:
        raise HTTPException(
            status_code=502,
            detail="AI servisi geçerli bir analiz sonucu döndürmedi."
        ) from ex

    feedback = Feedback(
        text=cleaned,
        sentiment=validated_result.sentiment,
        score=validated_result.score,
        summary=validated_result.summary,
        keywords=json.dumps(
            validated_result.keywords,
            ensure_ascii=False
        ),
        language=validated_result.language,
        category=validated_result.category
)

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return validated_result

def validate_input(text: str):

    cleaned_text = text.strip()

    if not cleaned_text:
        raise HTTPException(
            status_code=400,
            detail="Metin alanı boş olamaz."
        )

    if len(cleaned_text) < 10:
        raise HTTPException(
            status_code=400,
            detail="Metin analizi için içerik çok kısa."
        )

    return cleaned_text