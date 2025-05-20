from pydantic import BaseModel

class CreateProductDTO(BaseModel):
    name: str
    description: str
    category_id: str
    unit_price: float
    sale_price: float