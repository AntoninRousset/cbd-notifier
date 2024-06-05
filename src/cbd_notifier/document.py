from pydantic import BaseModel, Field
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
        return (
            f"[{self.symbol}] '{self.title.get('en', '<No english title available>')}'"
        )
