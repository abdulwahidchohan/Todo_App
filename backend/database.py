"""
Database setup for the Todo application using SQLModel.
For local development, using SQLite; for production, using Postgres.
"""

from sqlmodel import create_engine, Session
from contextlib import contextmanager
import os
from typing import Generator


# Database URL - using environment variable or default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create the engine
# For SQLite, we need to handle the URL differently
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.

    Yields:
        Session: Database session
    """
    with Session(engine) as session:
        yield session