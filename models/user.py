from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer, primary_key=True, index=True
    )
    username = Column(
        String, unique=True, index=True 
    )
    tg_id = Column(
        Integer, unique=True, index=True
    )

    notes = relationship(
        "Note",
        back_populates="user",
        cascade="all, delete-orphan"
    )


