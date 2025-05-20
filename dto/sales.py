from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import List

class GetSalesDTO(BaseModel):
    date_range: None | tuple[date, date] = None 
    limit: None | int = None
    offset: None | int = None
    product_id: None | str = None
    category_id: None | str = None

class GetSalesByDateRangeDTO(BaseModel):
    today: bool = False
    last_week: bool = False
    last_month: bool = False
    last_year: bool = False
    
class CompareSalesDTO(BaseModel):
    categories: List[str]
    today: bool = False
    last_week: bool = False
    last_month: bool = False
    last_year: bool = False

class CreateSaleDTO(BaseModel):
    date_created: date
    product_id: UUID
    quantity_sold: int
    total_bill: int
    
class UpdateSalesDTO(CreateSaleDTO):
    id: UUID
    
class DeleteSalesDTO(BaseModel):
    id: UUID    