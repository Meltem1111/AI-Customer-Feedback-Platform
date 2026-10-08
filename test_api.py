from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_feedbacks_endpoint():
    response = client.get("/feedbacks")

    assert response.status_code == 200

def test_feedbacks_stats_endpoint():
    response = client.get("/feedbacks/stats")

    assert response.status_code == 200

def test_analyze_empty_text():
    response = client.post(
        "/analyze",
        json={"text": ""}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Metin alanı boş olamaz."

def test_analyze_short_text():
    response = client.post(
        "/analyze",
        json={"text": "iyi"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Metin analizi için içerik çok kısa."

def test_invalid_min_score():
    response = client.get(
        "/feedbacks?min_score=101"
    )

    assert response.status_code == 422

def test_invalid_max_score():
    response = client.get(
        "/feedbacks?max_score=-1"
    )

    assert response.status_code == 422

def test_invalid_page():
    response = client.get(
        "/feedbacks?page=0"
    )

    assert response.status_code == 422

def test_invalid_page_size():
    response = client.get(
        "/feedbacks?page_size=0"
    )

    assert response.status_code == 422

def test_invalid_score_range():
    response = client.get(
        "/feedbacks?min_score=80&max_score=40"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "min_score, max_score değerinden büyük olamaz."

def test_feedbacks_response_structure():
    response = client.get("/feedbacks")

    assert response.status_code == 200

    data = response.json()

    assert "page" in data
    assert "page_size" in data
    assert "total" in data
    assert "total_pages" in data
    assert "items" in data

def test_feedback_item_structure():
    response = client.get("/feedbacks")

    assert response.status_code == 200

    data = response.json()

    if data["items"]:
        item = data["items"][0]

        assert "id" in item
        assert "text" in item
        assert "sentiment" in item
        assert "score" in item
        assert "summary" in item
        assert "keywords" in item
        assert "language" in item
        assert "category" in item
        assert "created_at" in item

def test_stats_response_structure():
    response = client.get("/feedbacks/stats")

    assert response.status_code == 200

    data = response.json()

    assert "positive" in data
    assert "negative" in data
    assert "neutral" in data
    assert "average_score" in data

def test_feedbacks_category_filter():
    response = client.get("/feedbacks?category=Ürün")

    assert response.status_code == 200

    data = response.json()

    for item in data["items"]:
        assert item["category"] == "Ürün"

def test_feedbacks_sentiment_filter():
    response = client.get("/feedbacks?sentiment=Pozitif")

    assert response.status_code == 200

    data = response.json()

    for item in data["items"]:
        assert item["sentiment"] == "Pozitif"

def test_feedbacks_search_filter():
    response = client.get("/feedbacks?search=yemek")

    assert response.status_code == 200

    data = response.json()

    for item in data["items"]:
        assert "yemek" in item["text"].lower()

def test_feedbacks_score_sort_asc():
    response = client.get(
        "/feedbacks?sort_by=score&sort_order=asc"
    )

    assert response.status_code == 200

    data = response.json()
    scores = [item["score"] for item in data["items"]]

    assert scores == sorted(scores)

def test_feedbacks_score_sort_desc():
    response = client.get(
        "/feedbacks?sort_by=score&sort_order=desc"
    )

    assert response.status_code == 200

    data = response.json()
    scores = [item["score"] for item in data["items"]]

    assert scores == sorted(scores, reverse=True)

def test_feedbacks_pagination():
    response = client.get(
        "/feedbacks?page=1&page_size=5"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["page_size"] == 5
    assert len(data["items"]) <= 5

def test_feedbacks_combined_filters_and_pagination():
    response = client.get(
        "/feedbacks?category=Ürün&sentiment=Pozitif&page=1&page_size=5"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["page_size"] == 5
    assert len(data["items"]) <= 5

    for item in data["items"]:
        assert item["category"] == "Ürün"
        assert item["sentiment"] == "Pozitif"

def test_stats_values():
    response = client.get("/feedbacks/stats")

    assert response.status_code == 200

    data = response.json()

    assert data["positive"] >= 0
    assert data["negative"] >= 0
    assert data["neutral"] >= 0

    assert 0 <= data["average_score"] <= 100