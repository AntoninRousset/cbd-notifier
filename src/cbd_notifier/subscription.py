from sqlmodel import Field, Relationship, SQLModel

from typing import TYPE_CHECKING

from cbd_notifier.chat import Chat

if TYPE_CHECKING:  # pragma: no cover
    from cbd_notifier.topic import Topic


class Subscription(SQLModel, table=True):
    chat_id: int = Field(foreign_key="chat.id", primary_key=True)
    chat: Chat = Relationship(back_populates="subscriptions")
    topic_name: str = Field(foreign_key="topic.name", primary_key=True)
    topic: "Topic" = Relationship(back_populates="subscriptions")
