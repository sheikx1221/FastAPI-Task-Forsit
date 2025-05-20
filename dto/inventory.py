from pydantic import BaseModel

class GetInventoryDTO(BaseModel):
    category_id: str | None = None
    product_id: str | None = None
    history: bool = False
    
class UpdateInventoryDTO(BaseModel):
    quantity: int
    product_id: str | None = None
    supplier_id: str | None = None