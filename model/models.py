from typing import Union

from pydantic import BaseModel, Field, RootModel


class Metadata(BaseModel):

    Summary: list[str] = Field(description="Summary of the document")

    Title: str = Field(description="Title of the document")

    Author: str = Field(description="Author of the document")

    DateCreated: str = Field(description="Date created of the document")

    LastModifiedDate: str = Field(description="Date modified of the document")

    Publisher: str = Field(description="Publisher of the document")

    Language: str = Field(description="Language of the document")

    PageCount: Union[int, str] = Field(description="Page count of the document")

    SentimentTone: str = Field(description="Sentiment of the document")


class ChangeFormat(BaseModel):

    Page: str

    changes: str


class SummaryResponse(RootModel[list[ChangeFormat]]):

    pass
