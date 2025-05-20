from pydantic import BaseModel

class GetInventoryDTO(BaseModel):
    category_id: str | None = None
    product_id: str | None = None
    history: bool = False
    limit: int = 10
    offset: int | None = None
class UpdateInventoryDTO(BaseModel):
    quantity: int
    product_id: str | None = None
    supplier_id: str | None = None
    
openapi_extra_GetInventoryDTO = {
    "parameters": [
        {
            "in": "query",
            "name": "category_id",
            "description": "match inventory with category id",
            "required": False,
            "schema": {
                "type": "string",
                "format": "uuid"
            }
        },
        {
            "in": "query",
            "name": "product_id",
            "description": "match inventory with product id",
            "required": False,
            "schema": {
                "type": "string",
                "format": "uuid"
            }
        },
        {
            "in": "query",
            "name": "history",
            "description": "if history of inventory is required, set it as true",
            "required": False,
            "schema": {
                "type": "boolean",
                "default": False
            }
        },
        {
            "in": "query",
            "name": "limit",
            "description": "find records with limit set",
            "required": False,
            "schema": {
                "type": "number",
                "default": "10"
            }
        },
        {
            "in": "query",
            "name": "offset",
            "description": "used for paginated response",
            "required": False,
            "schema": {
                "type": "number",
                "default": "0"
            }
        }
    ]
}