import asyncio
from datetime import timedelta
from typing import Annotated, Iterable

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)
import typer

from cbd_notifier.application import Application
from cbd_notifier.topic import Topic, TopicOrigin

DEFAULT_DATABASE_URL = "sqlite+aiosqlite:///cbd_notifier.db"
DEFAULT_TOPIC_POLL_INTERVAL = 60

app = typer.Typer()


async def _add_topic(
    name: str,
    urls: Iterable[str],
    db_sessionmaker: async_sessionmaker[AsyncSession],
) -> None:
    async with db_sessionmaker() as db_session:
        topic = Topic(origins=[TopicOrigin(url=url) for url in urls], name=name)
        db_session.add(topic)
        await db_session.commit()


@app.command()
def add_topic(
    name: str,
    urls: list[str],
    database_url: Annotated[
        str, typer.Option(envvar="DATABASE_URL")
    ] = DEFAULT_DATABASE_URL,
) -> None:
    db_engine = create_async_engine(database_url)
    db_sessionmaker = async_sessionmaker(db_engine)
    asyncio.run(_add_topic(name, urls, db_sessionmaker=db_sessionmaker))


async def _init(async_engine: AsyncEngine) -> None:
    async with async_engine.connect() as db_connection:
        await db_connection.run_sync(SQLModel.metadata.create_all)


@app.command()
def init(
    database_url: Annotated[
        str, typer.Option(envvar="DATABASE_URL")
    ] = DEFAULT_DATABASE_URL,
) -> None:
    db_engine = create_async_engine(database_url)
    asyncio.run(_init(db_engine))


@app.command()
def run(
    *,
    database_url: Annotated[
        str, typer.Option(envvar="DATABASE_URL")
    ] = DEFAULT_DATABASE_URL,
    poll_interval: float = DEFAULT_TOPIC_POLL_INTERVAL,
    token: Annotated[str, typer.Argument(envvar="TOKEN")],
) -> None:
    db_engine = create_async_engine(database_url)
    db_sessionmaker = async_sessionmaker(db_engine)
    Application(
        db_sessionmaker=db_sessionmaker,
        poll_interval=timedelta(seconds=poll_interval),
        token=token,
    ).run()


if __name__ == "__main__":
    app()
