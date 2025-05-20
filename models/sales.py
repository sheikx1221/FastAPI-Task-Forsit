import uuid
from database import Base
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, Column, Integer, DateTime, Double

class SalesBase(BaseModel):
    id: str
    date_created: datetime
    totalBill: int
    quantity_sold: int
    product_id: str
    
    class Config:
        from_attributes = True
    
class Sales(Base):
    __tablename__ = "tbl_Sale"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    date_created = Column(DateTime, default=func.now())
    totalBill = Column(Double)
    quantity_sold = Column(Integer)
    product_id = Column(UUID(as_uuid=True), ForeignKey("tbl_Product.id"))
    
    product = relationship("Product", back_populates="sales")