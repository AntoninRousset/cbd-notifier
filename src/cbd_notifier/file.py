from pydantic import BaseModel, Field, RootModel, create_model
from typing import Literal


class Document(BaseModel):
    id: str = Field(validation_alias="_id")
    symbol: str
    title: dict[Literal["en"], str]

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self) -> str:
        return f"[{self.symbol}] <Document> '{self.title.get('en', '<No english title available>')}'"


class DocumentList(RootModel):
    root: list[Document]


class Recommendation(BaseModel):
    id: str
    schema_s: Literal["recommendation"]
    symbol: str = Field(validation_alias="symbol_s")
    title: str = Field(validation_alias="title_s")

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self) -> str:
        return f"[{self.symbol}] <Recommendation> '{self.title}'"


class Notification(BaseModel):
    id: str
    meeting_ss: list[str]
    schema_s: Literal["notification"]
    symbol: str = Field(validation_alias="symbol_s")
    title: str = Field(validation_alias="title_s")

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self) -> str:
        return f"[{self.symbol}, {', '.join(self.meeting_ss)}] <Notification> '{self.title}'"


Index = Recommendation | Notification


class IndexList(BaseModel):
    response: create_model("IndexResponse", docs=(list[Index], ...))


File = Document | Recommendation | Notification
