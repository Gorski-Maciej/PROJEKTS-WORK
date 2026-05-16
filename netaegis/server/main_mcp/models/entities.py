from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, JSON
from server.shared.models import Base

class Incident(Base):
    __tablename__ = "incidents"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(80))
    status: Mapped[str] = mapped_column(String(20), default="open")
    source_mcp: Mapped[str] = mapped_column(String(80), default="unknown")
    payload: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
