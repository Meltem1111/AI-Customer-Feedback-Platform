from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Text, DateTime, text as sql_text


class Base(DeclarativeBase):
    pass

class Feedback(Base):
    __tablename__ = "Feedbacks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    sentiment = Column(String(20), nullable=False)
    score = Column(Integer, nullable=False)
    summary = Column(String(500))
    keywords = Column(Text)
    language = Column(String(10))
    category = Column(String(50))
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=sql_text("GETDATE()")
    )