# AI Customer Feedback Platform

AI Customer Feedback Platform is a web-based application that analyzes customer feedback using Google Gemini. The application performs sentiment analysis, generates a score and summary, extracts keywords, detects the language, and assigns a category to each feedback.

The analyzed feedback is stored in Microsoft SQL Server and can be viewed through the web dashboard.

## Features

- Sentiment analysis
- Sentiment score between 0 and 100
- Automatic summary generation
- Keyword extraction
- Language detection
- Feedback categorization
- Microsoft SQL Server integration
- Search and filtering
- Sorting
- Pagination
- Sentiment statistics
- Input validation
- REST API with FastAPI
- Web dashboard
- Automated API tests with Pytest

## Supported Categories

The application currently supports the following categories:

- `Restoran/Yemek`
- `Ürün`
- `Kargo/Teslimat`
- `Hizmet`
- `Diğer`

The model is mainly designed for Turkish customer reviews. Sentiment and category values are returned in Turkish.

## Dashboard

The project includes a simple web dashboard for interacting with the API.

The dashboard allows users to:

- Enter a customer review and analyze it
- View sentiment and score
- View the generated summary and keywords
- See the detected language and category
- Search existing feedback
- Filter feedback by sentiment and category
- Filter by score range
- Sort feedback by score or date
- Navigate between pages
- View general sentiment statistics

assets/dashboard.png

## Project Structure

```text
AI-Customer-Feedback-Platform/
│
├── analyzer.py
├── api.py
├── config.py
├── database.py
├── models.py
├── main.py
├── index.html
├── test_api.py
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE
```

File descriptions:

- `analyzer.py` - Sends feedback to Gemini and processes the AI response.
- `api.py` - Contains the FastAPI application and API endpoints.
- `config.py` - Loads application settings from environment variables.
- `database.py` - Creates the SQLAlchemy database connection and session.
- `models.py` - Contains the SQLAlchemy database model.
- `main.py` - Application entry point.
- `index.html` - Web dashboard.
- `test_api.py` - Automated API tests.

## Technologies

- Python 3.11
- FastAPI
- Google Gemini API
- Google GenAI SDK
- Pydantic
- SQLAlchemy
- Microsoft SQL Server
- ODBC Driver 18 for SQL Server
- PyODBC
- HTML
- JavaScript
- Tailwind CSS
- Pytest
- python-dotenv

## Prerequisites

The following software is required to run the project:

- Python 3.11
- Microsoft SQL Server
- SQL Server Management Studio (SSMS)
- ODBC Driver 18 for SQL Server
- Google Gemini API key

ODBC Driver 18 can be downloaded from Microsoft's official documentation:

https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server

## Installation

Clone the repository:

```bash
git clone https://github.com/Meltem1111/AI-Customer-Feedback-Platform.git
cd AI-Customer-Feedback-Platform
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root.

The repository contains a `.env.example` file that can be used as a template.

Example:

```text
GEMINI_API_KEY=your_gemini_api_key_here

MODEL_NAME=gemini-2.5-flash
TEMPERATURE=0.2

DB_SERVER=your_sql_server
DB_NAME=AI_Customer_Feedback
```

The `.env` file should never be committed to GitHub because it contains sensitive configuration such as the Gemini API key.

## Database Setup

The application uses Microsoft SQL Server.

First, create the database:

```sql
CREATE DATABASE AI_Customer_Feedback;
```

Then create the `Feedbacks` table:

```sql
USE AI_Customer_Feedback;

CREATE TABLE Feedbacks (
    id INT IDENTITY(1,1) PRIMARY KEY,
    text NVARCHAR(MAX) NOT NULL,
    sentiment NVARCHAR(20) NOT NULL,
    score INT NOT NULL,
    summary NVARCHAR(MAX),
    keywords NVARCHAR(MAX),
    language NVARCHAR(20),
    category NVARCHAR(50),
    created_at DATETIME DEFAULT GETDATE()
);
```

The application uses SQLAlchemy and ODBC Driver 18 to connect to SQL Server.

Database connection settings are read from the `.env` file:

```text
DB_SERVER=your_sql_server
DB_NAME=AI_Customer_Feedback
```

The current configuration uses a Windows Trusted Connection instead of storing a database password in the project.

## Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Running the Dashboard

After starting the FastAPI server, open `index.html` in a web browser.

The dashboard sends requests to the FastAPI backend.

CORS is enabled in the FastAPI application so that the locally opened dashboard can communicate with the backend.

## API Endpoints

### POST /analyze

Analyzes a customer feedback and saves the result to the database.

Example request:

```json
{
    "text": "Ürün çok kaliteli ve hızlı teslim edildi."
}
```

Example response:

```json
{
    "sentiment": "Pozitif",
    "score": 95,
    "summary": "Ürün kaliteli ve hızlı teslim edildi.",
    "keywords": [
        "ürün",
        "kalite",
        "teslimat",
        "hızlı",
        "memnuniyet"
    ],
    "language": "tr",
    "category": "Ürün"
}
```

### GET /feedbacks

Returns stored feedback.

Basic request:

```text
/feedbacks?page=1&page_size=10
```

Example response:

```json
{
    "page": 1,
    "page_size": 10,
    "total": 3,
    "total_pages": 1,
    "items": [
        {
            "id": 1,
            "text": "Ürün çok kaliteli ve hızlı teslim edildi.",
            "sentiment": "Pozitif",
            "score": 95,
            "summary": "Ürün kaliteli ve hızlı teslim edildi.",
            "keywords": [
                "ürün",
                "kalite",
                "teslimat",
                "hızlı",
                "memnuniyet"
            ],
            "language": "tr",
            "category": "Ürün",
            "created_at": "2026-10-01T15:30:00"
        }
    ]
}
```

The endpoint also supports filtering and sorting.

Examples:

```text
/feedbacks?sentiment=Pozitif
```

```text
/feedbacks?category=Ürün
```

```text
/feedbacks?min_score=70&max_score=100
```

```text
/feedbacks?search=yemek
```

```text
/feedbacks?sort_by=score&sort_order=desc
```

### GET /feedbacks/stats

Returns general sentiment statistics.

Example response:

```json
{
    "positive": 15,
    "negative": 4,
    "neutral": 6,
    "average_score": 74.6
}
```

## Testing

The project contains automated API tests using Pytest.

Activate the virtual environment and run:

```bash
pytest
```

The tests cover:

- Feedback endpoint
- Statistics endpoint
- Input validation
- Pagination
- Sentiment filtering
- Category filtering
- Search
- Score sorting
- Combined filters
- Response structure
- Invalid score ranges

The current tests do not send valid feedback to Gemini. Therefore, running the test suite does not consume Gemini API quota.

## Security

Sensitive configuration is stored in environment variables.

The following values are not stored directly in the source code:

- Gemini API key
- Database server
- Database name

The `.env` file is included in `.gitignore`.

API keys and other sensitive credentials should never be committed to the repository.

## Current Status

The main application is functional.

Implemented features:

- Sentiment analysis
- Sentiment scoring
- Summary generation
- Keyword extraction
- Language detection
- Feedback categorization
- FastAPI backend
- SQL Server integration
- Database persistence
- Search
- Filtering
- Sorting
- Pagination
- Statistics
- Input validation
- Automated API tests
- Web dashboard

## Future Improvements

Possible improvements for future versions include:

- Sentiment trend analysis over time
- Bulk CSV feedback upload
- Docker support
- More detailed dashboard analytics
- AI-generated customer insights
- User authentication
- Cloud deployment
- Automated reports and notifications

## License

This project is licensed under the MIT License.

See the `LICENSE` file for more information.

## Author

Meltem

Computer Engineering Student

GitHub: https://github.com/Meltem1111

LinkedIn: Add your LinkedIn profile here

## Project Goal

The main goal of this project is to build a practical application that combines generative AI, backend development, database management, and a web interface.

The project demonstrates how customer feedback can be analyzed with an AI model, converted into structured data, stored in a relational database, and presented through an API and web dashboard.