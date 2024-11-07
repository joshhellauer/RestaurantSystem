# models.py

from sqlalchemy import Column, String, Integer, Float, ForeignKey, create_engine, JSON
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()
BaseOrders = declarative_base()
class Order(BaseOrders):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    order_data = Column(JSON)

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    calories = Column(Integer)
    image=Column(String)
    price= Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")

# Set up the database engine
DATABASE_URL = "sqlite:///app.db"
engine = create_engine(DATABASE_URL, echo=True)
ORDER_DATABASE_URL = "sqlite:///orders.db"
orders_engine = create_engine(ORDER_DATABASE_URL, echo=True)
# Create tables
Base.metadata.create_all(bind=engine)
BaseOrders.metadata.create_all(bind=orders_engine)

# Create a session
Session = sessionmaker(bind=engine)
SessionOrders = sessionmaker(bind=orders_engine)
