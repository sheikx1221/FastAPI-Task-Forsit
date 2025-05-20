# E-Commerce FastAPI Server

An e-commerce application that allows you to track sales by time range, do revenue analysis and compare sales/revenue between categories.

The application also help you track inventory, get sale/purchase history by passing a single flag and also add/remove stock levels

## Key Features
- Get Sales for
    - today
    - last_week
    - last_month
    _ last_year
- Find all sales by category
- Find all sales by product
- Paginated results
- Comparison of Sales by Categories
    - Send as many categories as you want
    - API will calculate total_bill amount

- Get Inventory
    - By Category
    - By Product
    - Request history (sold and purchased)
    - Increase/Decrease stock

- Product
    - Register new product with already existing categories
    - add stock using /inventory/update endpoint

## requirements.txt aka Dependencies
```
annotated-types==0.7.0
anyio==4.9.0
click==8.2.0
dotenv==0.9.9
Faker==37.3.0
fastapi==0.115.12
h11==0.16.0
idna==3.10
psycopg2-binary==2.9.10
pydantic==2.11.4
pydantic_core==2.33.2
python-dotenv==1.1.0
sniffio==1.3.1
SQLAlchemy==2.0.41
starlette==0.46.2
typing-inspection==0.4.0
typing_extensions==4.13.2
tzdata==2025.2
uuid==1.30
uvicorn==0.34.2
```

## Setup guide
- Clone the repository locally
- If you are using python > 3.x, you will need to create virtual env, copy paste the below command after cloning repository  
`python3 -m venv .venv`
- Install libraries  
`pip install -r requirements.txt`
- After installing, set .env file, shared on email with hosted database path
- To use local db, just replace `DATABASE_URL` inside .env with local db url  
`DATABASE_URL = postgres:user:password@localhost:5432/db_name`
- If using local database run the following command to seed test data in database  
`python seed.py`
- Once done run the server using the following command  
`uvicorn main:app --reload`

## API Documentation
I have fixed Swagger documentation and you can directly test all endpoints from there.  
Open the following link on your browser
`http://127.0.0.1:8000/docs`