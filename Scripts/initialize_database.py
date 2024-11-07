import json
from sqlalchemy.orm import sessionmaker
from models import Category, Product, engine, orders_engine, BaseOrders

# Read JSON data
with open('product_data.json', 'r') as file:
    categories_data = json.load(file)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()
SessionOrders = sessionmaker(bind=orders_engine)
BaseOrders.metadata.create_all(bind=orders_engine)
# Add categories and products to the database
for category_data in categories_data:
    # Extract category information
    category_name = category_data['name']
    
    # Check if the category already exists in the database
    existing_category = session.query(Category).filter_by(name=category_name).first()

    if not existing_category:
        # Category doesn't exist, add it to the database
        new_category = Category(name=category_name)
        session.add(new_category)
        session.commit()  # Commit the category before adding products

        # Add products to the database
        for product_info in category_data.get('products', []):
            new_product = Product(
                name=product_info['name'],
                description=product_info.get('description', ''),
                calories=product_info.get('calories', 0),
                image=product_info.get('image', ''),
                price=product_info.get('price', 0),
                category_id=new_category.id
            )
            session.add(new_product)

# Commit and close the session
session.commit()
session.close()
