# jagriti-case-engine
A data pipeline project that extracts case information from the e-Jagriti portal, stores it in PostgreSQL, and exposes it through a FastAPI service.

This project demonstrates practical backend development skills including:
- API discovery and reverse-engineering using browser developer tools
- Data ingestion using Python
- Database storage and management
- REST API development with FastAPI

---

## How Data is Collected

Instead of scraping HTML pages, the system directly calls an **open API endpoint used internally by the e-Jagriti portal**.

The endpoint returns structured **JSON data**, which makes the extraction process more reliable and efficient than HTML scraping.

Example API endpoint:

https://e-jagriti.gov.in/services/report/report/getCauseTitleListByCompany

Example query:

https://e-jagriti.gov.in/services/report/report/getCauseTitleListByCompany?commissionTypeId=1&commissionId=11000000&filingDate1=2025-01-01&filingDate2=2026-03-13&complainant_respondent_name_en=biswas

---

## Data Collection Workflow

The scraper script works as follows:

1. Prompt user for:
   - complainant/respondent name
   - filing start date
   - filing end date
2. Send an HTTP request to the e-Jagriti API using the `requests` library
3. Receive case records in JSON format
4. Extract required fields from the response
5. Store the data in the PostgreSQL table `e_jagriti_cases`

---

## Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy (Async ORM)

### Database
- PostgreSQL

### Data Ingestion
- Python Requests

### API Server
- Uvicorn

---

## Project Architecture

e_jagriti_project
│
├── api
│ ├── main.py
│ ├── routes
│ │ └── cases.py
│ ├── schemas
│ │ └── case_schema.py
│ └── dependencies
│ └── database.py
│
├── models
│ └── case_model.py
│
├── scraper
│ └── scrape_cases.py
│
├── requirements.txt
├── .gitignore
└── README.md

---

## Database Schema

Table: **e_jagriti_cases**

| Column | Type | Description | 
|------|------|-------------|
| case_no | VARCHAR | Unique case identifier | 
| complainant | TEXT | Name of complainant |
| respondent | TEXT | Name of respondent |
| filing_date | DATE | Case filing date |
| first_hearing | DATE | First hearing date |
| next_hearing | DATE | Next hearing date |
| stage | VARCHAR | Current case stage |
| scraped_at | TIMESTAMPTZ | Timestamp when record was stored |

---

## API Endpoints

### 1. List Cases

Retrieve stored cases with optional pagination.

Endpoint

GET /api/v1/cases

Query Parameters

| Parameter | Description |
|----------|-------------|
| limit | Number of records to return |
| offset | Number of records to skip |

Example

GET /api/v1/cases?limit=10&offset=0

### 2. Get Case By Case Number

Retrieve details for a specific case.

Endpoint

GET /api/v1/cases/case_no/{case_no}

Example

GET /api/v1/cases/case_no/NC/RP/117/2026

### 3. Search Cases

Search cases by complainant or respondent name.

Endpoint

GET /api/v1/cases/search

Example

GET /api/v1/cases/search?query=LIPIMITA

---

## Running the Project

### 1. Clone the repository

git clone https://github.com/sayaksamanta10176/jagriti-case-engine.git
cd jagriti-case-engine

### 2. Install dependencies
pip install -r requirements.txt


### 3. Configure Database

Create a PostgreSQL database.

Example:
e_jagriti_db(my database name is postgres)

Update the database connection string in the environment configuration.
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/jagriti_db

### 5. Run the FastAPI Server
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000

Server will start at
http://127.0.0.1:8000

---

## Future Improvements

- Automate data ingestion with scheduled jobs
- Add unit testing with Pytest
- Implement caching for faster responses
- Containerize the application with Docker

---

## Author

Sayak Samanta  
Python Backend Developer