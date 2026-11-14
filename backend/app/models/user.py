
from datetime import datetime

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):

    __tablename__ = "users"

    # Unique identifier for every user
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    # User's full name
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    # Email must be unique
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    # Store the hashed password, never the original password
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # Automatically record account creation time
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
