from pydantic import BaseModel, Field
from datetime import date


class Rule(BaseModel):
    id: str
    name: str
    status: str
    author: str
    version: str = Field(coerce_numbers_to_str=True)
    date: date
    confidence: float
    variables: dict[str, str | list]
    description: str
    query: str
    tags: list[str]
    data_source: dict
    level: str
    references: list[str]
    robustness: str
    false_positives: str | None = None
    blindspots: str | None = None
    response_plan: str | None = None
