from datetime import datetime, timedelta
from fastapi import Request
from database import get_db
from sqlalchemy import desc, func
from models import Sales, Product
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from dto.sales import GetSalesDTO, GetSalesByDateRangeDTO, CompareSalesDTO

router = APIRouter(prefix="/sales", tags=["sales"])
session: Session = Depends(get_db)

@router.get("/list/")
async def getSales(request: Request, db = session):
    params = dict(request.query_params)
    dto = GetSalesDTO(**params)
    
    query = db.query(Sales).options(
        joinedload(Sales.product).joinedload(Product.category)
    )
    query = query.join(Sales.product).join(Product.category)
    
    if dto.date_range:
        start_date, end_date = dto.date_range
        query = query.filter(Sales.date_created.between(start_date, end_date))
        
    if dto.category_id:
        query = query.filter(Product.category_id == dto.category_id)
    elif dto.product_id:
        query = query.filter(Product.id == dto.product_id)
    
    query = query.order_by(desc(Sales.date_created))
    
    if dto.offset:
        query = query.offset(dto.offset)
        
    limit = dto.limit if dto.limit else 10
    query = query.limit(limit)
    
    return query.all()

@router.get("/range/")
def getSalesInRange(request: Request, db = session):
    params = dict(request.query_params)
    dto = GetSalesByDateRangeDTO(**params)
    
    query = db.query(Sales).options(
        joinedload(Sales.product).joinedload(Product.category)
    )
    query = query.join(Sales.product).join(Product.category)
    
    today = datetime.now().date()
    if dto.today:
        query = query.filter(func.date(Sales.date_created) == today)
    elif dto.last_week:
        week_ago = today - timedelta(days=7)
        query = query.filter(Sales.date_created.between(week_ago, today))
    elif dto.last_month:
        month_ago = today - timedelta(days=30)
        query = query.filter(Sales.date_created.between(month_ago, today))
    elif dto.last_year:
        year_ago = today - timedelta(days=365)
        query = query.filter(Sales.date_created.between(year_ago, today))
    
    query = query.order_by(desc(Sales.date_created))
    return query.all()

@router.post("/compare/")
def compareRevenue(body: CompareSalesDTO, db = session):
    salesDict = {}
    today = datetime.now().date()
    start_date = None
    end_date = None
    
    if body.today:
        start_date = today
        end_date = today
    elif body.last_week:
        start_date = today - timedelta(days=7)
        end_date = today
    elif body.last_month:
        start_date = today - timedelta(days=30)
        end_date = today
    elif body.last_year:
        start_date = today - timedelta(days=365)
        end_date = today

    for category_id in body.categories:
        query = (
            db.query(
                Product.category_id,
                func.sum(Sales.totalBill).label('total_bill')
            )
            .join(Sales.product)
            .join(Product.category)
            .filter(Product.category_id == category_id)
        )
        
        if start_date and end_date:
            query = query.filter(func.date(Sales.date_created).between(start_date, end_date))
            
        query = query.group_by(Product.category_id)
        result = query.first()
        
        if result:
            salesDict[str(category_id)] = {
                'total_bill': float(result.total_bill or 0)
            }
        else:
            salesDict[str(category_id)] = {
                'total_bill': 0.0
            }

    return salesDict