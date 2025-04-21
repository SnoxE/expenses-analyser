from fastapi import Query, HTTPException
from typing import Optional, Any
from utils import MONTHS


def validate_and_retrieve_period(
    period: Optional[str] = Query(None),
) -> tuple[str | None, Any | None]:
    if not period:
        return None, None

    period = period.strip().capitalize()

    if period in MONTHS:
        return "month", period
    elif period.isdigit() and int(period) in [1, 2, 3, 4]:
        return "quarter", int(period)

    raise HTTPException(
        status_code=422,
        detail=f"Invalid period '{period}'. Must be a month name (e.g., Jan) or quarter number (1–4).",
    )
