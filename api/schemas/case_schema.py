from pydantic import BaseModel
from datetime import date, datetime

class CaseResponse(BaseModel):
    case_no: str
    complainant: str
    respondent: str | None
    filing_date: date
    first_hearing: date | None
    next_hearing: date | None
    stage: str | None
    scraped_at: datetime

    class Config:
        from_attributes = True