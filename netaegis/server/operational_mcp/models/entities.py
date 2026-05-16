from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, JSON, Boolean
from server.shared.models import Base

class LocalEvent(Base):
    __tablename__ = "local_events"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(80))
    payload: Mapped[dict] = mapped_column(JSON, default={})
    synced: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
