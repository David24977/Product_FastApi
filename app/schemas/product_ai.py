from pydantic import BaseModel


class ProductAIAnalysisResponse(BaseModel):
    category: str
    tags: list[str]
    price_evaluation: str


class ProductAIAnalysisFullResponse(BaseModel):
    category: str
    tags: list[str]
    price_evaluation: str
    stock_status: str
