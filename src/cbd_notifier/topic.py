from collections import defaultdict
from httpx import AsyncClient
from pydantic import TypeAdapter
from sqlmodel import Field, Relationship, SQLModel
from typing import ClassVar
from typing import AsyncIterator

from cbd_notifier.file import DocumentList, IndexList, File
from cbd_notifier.subscription import Subscription


class TopicOrigin(SQLModel, table=True):
    topic_name: str = Field(foreign_key="topic.name", primary_key=True)
    topic: "Topic" = Relationship(back_populates="origins")
    url: str = Field(primary_key=True)

    @property
    def files(self):
        return Topic._files[self.topic_name]

    async def poll(self, client) -> AsyncIterator[File]:
        response = await client.get(self.url)
        data = TypeAdapter(DocumentList | IndexList).validate_json(response.content)
        files = data.root if isinstance(data, DocumentList) else data.response.docs

        for file in files:
            if file not in self.files:
                yield file
                self.files.add(file)


class Topic(SQLModel, table=True):
    _files: ClassVar[defaultdict[str, set[File]]] = defaultdict(set)

    name: str = Field(primary_key=True)
    subscriptions: list[Subscription] = Relationship(back_populates="topic")
    origins: list[TopicOrigin] = Relationship(back_populates="topic")

    async def poll(self, client: AsyncClient) -> AsyncIterator[File]:
        for origin in self.origins:
            async for file in origin.poll(client):
                yield file
