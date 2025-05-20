import uuid
from sqlalchemy import func
from database import get_db
from models import Inventory, Product
from sqlalchemy.orm import Session, joinedload
from fastapi import APIRouter, Depends, Request, HTTPException
from dto.inventory import GetInventoryDTO, UpdateInventoryDTO
from dto.inventory import openapi_extra_GetInventoryDTO

router = APIRouter(prefix="/inventory", tags=["Inventory"])
session: Session = Depends(get_db)

@router.get('/list', openapi_extra=openapi_extra_GetInventoryDTO, )
def getList(request: Request, db = session):
    params = dict(request.query_params)
    dto = GetInventoryDTO(**params)
    
    query = (
        db.query(Product)
        .options(joinedload(Product.category))
        .join(Product.category)
    )
    
    if dto.category_id:
        query = query.filter(Product.category_id == dto.category_id)
    elif dto.product_id:
        query = query.filter(Product.id == dto.product_id)
    
    if (dto.offset):
        query = query.offset(dto.offset)
    
    products = query.limit(dto.limit).all()
    result = []

    for product in products:
        current_stock = db.query(
            func.coalesce(func.sum(Inventory.quantity), 0)
        ).filter(
            Inventory.product_id == product.id
        ).scalar()
        
        setattr(product, 'current_stock', int(current_stock))
        
        if (dto.history):
            hquery = db.query(Inventory).filter(Inventory.product_id == product.id).all()
            setattr(product, 'history', hquery)
        
        result.append(product)
    
    return result

@router.put("/update/")
def updateInventory(body: UpdateInventoryDTO, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == body.product_id).first()
    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"Product with id {body.product_id} not found"
        )
    
    new_inventory = Inventory(
        id=uuid.uuid4(),
        quantity=body.quantity,
        product_id=body.product_id,
        supplier_id=body.supplier_id if body.supplier_id else None
    )
    
    try:
        db.add(new_inventory)
        db.commit()
        db.refresh(new_inventory)
        return {
            "message": "Inventory updated successfully",
            "inventory": new_inventory
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error updating inventory: {str(e)}"
        )