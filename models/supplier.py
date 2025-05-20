import uuid
from database import Base
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, UUID, String

class SupplierBase(BaseModel):
    id: str
    name: str
    address: str = None
    phone: str = None
    
class Supplier(Base):
    __tablename__ = "tbl_Supplier"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    address = Column(String, default="")
    phone = Column(String, default="")
    
    inventories = relationship("Inventory", back_populates="supplier")