from pydantic import BaseModel


class AggregationResult(BaseModel):
    total: str
