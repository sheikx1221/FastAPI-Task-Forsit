import uuid
from models import Product
from database import get_db
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from dto.product import CreateProductDTO

router = APIRouter(prefix="/product", tags=["Product"])
session: Session = Depends(get_db)

@router.post("/register/")
def register_product(body: CreateProductDTO, db: Session = Depends(get_db)):
    new_product = Product(
        id=uuid.uuid4(),
        name=body.name,
        descrition=body.description,
        unit_price=body.unit_price,
        sale_price=body.sale_price,
        category_id=body.category_id
    )
    
    try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error creating product: {str(e)}"
        )