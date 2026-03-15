from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from ..core.databases import get_session
from ..models.case_model import Case
from ..schemas.case_schema import CaseResponse

router = APIRouter(prefix="/api/v1/cases", tags=["Cases"])

# List Cases Endpoint
@router.get("", response_model=list[CaseResponse])
async def list_cases(
    limit: int | None = Query(None, ge=1),   
    offset: int | None = Query(None, ge=0),
    session: AsyncSession = Depends(get_session)
):
    query = (select(Case).limit(limit).offset(offset))
    result = await session.execute(query)
    cases = result.scalars().all()

    return cases

# Get Case by ID Endpoint
@router.get("/case_no/{case_no:path}", response_model=CaseResponse)
async def get_case_by_id(
    case_no: str,
    session: AsyncSession = Depends(get_session)
):
    query = select(Case).where(Case.case_no == case_no)
    result = await session.execute(query)
    case = result.scalar_one_or_none()

    if case is None:
        raise HTTPException(
            status_code=404,
            detail=f"Case with case_no '{case_no}' not found"
        )

    return case

# Search Cases
@router.get("/search", response_model=list[CaseResponse])
async def search_cases(
    q: str = Query(..., min_length=1),
    session: AsyncSession = Depends(get_session)
):
    search_term = f"%{q}%"

    query = select(Case).where(
        or_(
            Case.complainant.ilike(search_term),
            Case.respondent.ilike(search_term)
        )
    )

    result = await session.execute(query)
    cases = result.scalars().all()

    return cases