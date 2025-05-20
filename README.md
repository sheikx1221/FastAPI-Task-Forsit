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