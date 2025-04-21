from typing import Any

from fastapi import FastAPI, Request, Query, HTTPException, Depends

from utils import process_expenses
from dependencies import validate_and_retrieve_period
from models import AggregationResult

app = FastAPI()


@app.post("/api/aggregate")
async def aggregate(
    request: Request,
    department: str = Query(...),
    year: int = Query(None),
    period_data: tuple[str | None, Any | None] = Depends(validate_and_retrieve_period),
) -> AggregationResult:
    try:
        body = await request.body()
        csv_text = body.decode("utf-8")
        period_type, period_value = period_data

        result = process_expenses(csv_text, department, year, period_type, period_value)
        return AggregationResult(total=result)

    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="Unable to process the request due to an unexpected error: "
            + str(e),
        )
