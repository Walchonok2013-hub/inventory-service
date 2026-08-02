
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, String
from sqlalchemy.orm import relationship
from .base import Base

class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    quantity_initial = Column(Float, nullable=False)
    quantity_remaining = Column(Float, nullable=False)
    purchased_at = Column(DateTime, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    storage_location = Column(String)
    price = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="batches")
    operations = relationship("Operation", back_populates="batch")