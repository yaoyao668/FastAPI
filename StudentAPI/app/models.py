from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class Student(SQLModel, table=True ):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "students"

    id: int | None = Field(primary_key=True, default=None)
    name: str
    group_id: Optional[int] = Field(default=None, foreign_key="groups.id")
    group: Optional["Group"] = Relationship(back_populates="students")

class Group(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "groups"
    id: int | None = Field(primary_key=True, default=None)
    name: str
    students: List[Student] = Relationship(back_populates="group")
