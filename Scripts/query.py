# query.py

import pandas as pd
from sqlalchemy import create_engine, text

# Replace 'your_database_here' with the actual path to your SQLite database file
DATABASE_URL = "sqlite:///app.db"
ORDERS_URL = "sqlite:///orders.db"
# Create a database engine
engine = create_engine(DATABASE_URL, echo=True)
orders_engine = create_engine(ORDERS_URL, echo=True)
order_query = text("""SELECT o.id as order_id, o.name as order_name, o.order_data as order_data 
FROM orders o
""")
# Define a simple query to retrieve all categories and products
query = text("""
SELECT c.name as category_name, p.name as product_name, p.description, p.calories, p.image, p.price
FROM categories c
JOIN products p ON c.id = p.category_id
""")

# Execute the query and load the results into a pandas DataFrame
with engine.connect() as conn:
    result = conn.execute(query)
    df = pd.DataFrame(result.fetchall(), columns=result.keys())

with orders_engine.connect() as conn:
    result = conn.execute(order_query)
    for row in result:
        order_id, order_name, order_data = row
        print(row)
        # Process the retrieved data as needed
# Print the DataFrame
print(df)
