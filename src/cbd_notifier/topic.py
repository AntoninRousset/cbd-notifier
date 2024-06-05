from collections import defaultdict
import httpx
from pydantic import TypeAdapter
from sqlmodel import Field, Relationship, SQLModel
from typing import ClassVar

from cbd_notifier.document import Document
from cbd_notifier.subscription import Subscription


class Topic(SQLModel, table=True):
    _documents: ClassVar[defaultdict[str, set[Document]]] = defaultdict(set)
    name: str = Field(primary_key=True)
    subscriptions: list[Subscription] = Relationship(back_populates="topic")
    url: str

    @property
    def documents(self):
        return Topic._documents[self.name]

    async def poll(self) -> list[Document]:
        async with httpx.AsyncClient() as client:
            response = await client.get(self.url)
            documents = TypeAdapter(list[Document]).validate_json(response.content)

            for document in documents:
                if document not in self.documents:
                    yield document
                    self.documents.add(document)
