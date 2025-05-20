import uuid
from database import Base
from pydantic import BaseModel
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, Integer, Column, DateTime

class InventoryBase(BaseModel):
    id: str
    date_purchased: str
    quantity: int  
    supplier_id: str

    class Config:
            from_attributes = True

class Inventory(Base):
    __tablename__ = "tbl_Inventory"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    date_purchased = Column(DateTime, default=func.now())
    quantity = Column(Integer)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey('tbl_Supplier.id'))
    product_id = Column(UUID(as_uuid=True), ForeignKey('tbl_Product.id'))
    
    supplier = relationship("Supplier", back_populates="inventories")
    product = relationship("Product", back_populates="products")