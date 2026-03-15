from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Text, Date, TIMESTAMP

Base = declarative_base()

class Case(Base):
    __tablename__ = "e_jagriti_cases"   
    
    case_no = Column(String(255), primary_key=True)
    complainant = Column(Text)
    respondent = Column(Text)
    filing_date = Column(Date)
    first_hearing = Column(Date)
    next_hearing = Column(Date)
    stage = Column(String(100))
    scraped_at = Column(TIMESTAMP(timezone=True))