from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import List, Optional

class GetSalesDTO(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    product_id: Optional[str] = None
    category_id: Optional[str] = None

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
    
    
openapi_extra_GetSalesDTO = {
    "parameters": [
        {
            "in": "query",
            "name": "start_date",
            "description": "Start date for sales records (YYYY-MM-DD)",
            "required": False,
            "schema": {
                "type": "string",
                "format": "date"
            }
        },
        {
            "in": "query",
            "name": "end_date",
            "description": "End date for sales records (YYYY-MM-DD)",
            "required": False,
            "schema": {
                "type": "string",
                "format": "date"
            }
        },
        {
            "in": "query",
            "name": "limit",
            "description": "Number of records to return",
            "required": False,
            "schema": {
                "type": "integer",
                "default": 10
            }
        },
        {
            "in": "query",
            "name": "offset",
            "description": "Number of records to skip",
            "required": False,
            "schema": {
                "type": "integer",
                "default": 0
            }
        },
        {
            "in": "query",
            "name": "product_id",
            "description": "Filter by product ID",
            "required": False,
            "schema": {
                "type": "string",
                "format": "uuid"
            }
        },
        {
            "in": "query",
            "name": "category_id",
            "description": "Filter by category ID",
            "required": False,
            "schema": {
                "type": "string",
                "format": "uuid"
            }
        }
    ]
}

openapi_extra_GetSalesByDateRangeDTO = {
    "parameters": [
        {
            "in": "query",
            "name": "today",
            "description": "get sales records for today",
            "required": False,
            "schema": {
                "type": "boolean",
                "default": "false"
            }
        },
        {
            "in": "query",
            "name": "last_week",
            "description": "get sales records for last_week",
            "required": False,
            "schema": {
                "type": "boolean",
                "default": "false"
            }
        },
        {
            "in": "query",
            "name": "last_month",
            "description": "get sales records for last month",
            "required": False,
            "schema": {
                "type": "boolean",
                "default": "false"
            }
        },
        {
            "in": "query",
            "name": "last_year",
            "description": "get sales records for last_year",
            "required": False,
            "schema": {
                "type": "boolean",
                "default": "false"
            }
        }
    ]
}