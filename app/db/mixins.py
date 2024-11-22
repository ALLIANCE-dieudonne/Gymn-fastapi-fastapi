from datetime import datetime, UTC
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declared_attr

class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=datetime.now(UTC), nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC), nullable=False)