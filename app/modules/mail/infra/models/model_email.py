from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.orm import Mapped
from typing import Optional, List

class BaseEmail(SQLModel, table=False):
    subject: str = Field(nullable=False, max_length=55, min_length=1)
    from_email: str
    to_email: str
    content: str
    is_deleted: bool = Field(default=False)

class HeadEmailTable(BaseEmail, table=True):
    __tablename__ = "head_email"
    id: Optional[int] = Field(default=None, primary_key=True)

    replys: Mapped[List['ReplyEmailTable']] = Relationship(
        back_populates="head_email",
        sa_relationship_kwargs={
            "cascade": "delete, all-orphan",
            "lazy": "selectin"
        }
    )

class ReplyEmailTable(BaseEmail, table=True):
    __tablename__ = "reply_email"
    id: Optional[int] = Field(default=None, primary_key=True)
    head_email_id: Optional[int] = Field(default=None, foreign_key="head_email.id")
    head_email: Mapped[Optional[HeadEmailTable]] = Relationship(
        back_populates="replys"
    )