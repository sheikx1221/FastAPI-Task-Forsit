from database import Base
from pydantic import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

class CategoryBase(BaseModel):
    id: str
    name: str
    description: str
    
    class Config:
        from_attributes = True
    
class Category(Base):
    __tablename__ = "tbl_Category"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String)
    descrition = Column(String)
    
    products = relationship("Product", back_populates="category")