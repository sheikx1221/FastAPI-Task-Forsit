from database import Base
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, Column, String, Double

class ProductBase(BaseModel):
    id: str
    name: str
    description: str
    unit_price: int
    sale_price: int
    category_id: str
    
    class Config:
        from_attributes = True
    
class Product(Base):
    __tablename__ = "tbl_Product"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String)
    descrition = Column(String)
    unit_price = Column(Double)
    sale_price = Column(Double)
    category_id = Column(UUID(as_uuid=True), ForeignKey("tbl_Category.id"))
    
    category = relationship("Category", back_populates="products")
    sales = relationship("Sales", back_populates="product")
    products = relationship("Inventory", back_populates="product")
    