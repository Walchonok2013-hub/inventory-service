from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class OperationType(Enum):
    purchase = "purchase"
    consume = "consume"
    discard = "discard"
    correction = "correction"
    transfer = "transfer"

class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id", ondelete="SET NULL"), nullable=True, index=True)
    operation_type = Column(String, nullable=False)  # храним как строку для простоты
    quantity = Column(Float, nullable=False)
    comment = Column(String)
    idempotency_key = Column(String, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="operations")
    batch = relationship("Batch", back_populates="operations")