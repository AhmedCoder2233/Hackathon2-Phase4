import os
from datetime import datetime, timezone
from typing import List, Optional, Generator

from dotenv import load_dotenv
from sqlmodel import Field, Relationship, SQLModel, Session as SQLModelSession, create_engine

load_dotenv()


class User(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    emailVerified: bool = Field(default=False)
    image: Optional[str] = None
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    sessions: List["UserSession"] = Relationship(back_populates="user")


class UserSession(SQLModel, table=True):
    __tablename__ = "session"
    
    id: Optional[str] = Field(default=None, primary_key=True)
    userId: str = Field(foreign_key="user.id")
    expiresAt: datetime
    token: str
    ipAddress: Optional[str] = None
    userAgent: Optional[str] = None
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: Optional[User] = Relationship(back_populates="sessions")


class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_message"
    
    id: Optional[str] = Field(default=None, primary_key=True)
    userId: str
    role: str
    content: str
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Task(SQLModel, table=True):
    __tablename__ = "task"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[SQLModelSession, None, None]:
    with SQLModelSession(engine) as session:
        yield session