from pydantic import BaseModel, Field


class Metadata(BaseModel):
    summary: str = Field(description="Summary of the document")
    keywords: list[str] = Field(description="Keywords extracted from the document")
