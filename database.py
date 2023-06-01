from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL="postgresql://halal_db_user:fZ4ueRxMA0s7v4XoeCbsDcaY5kPRRShp@dpg-chsbkk8rddl7atarimu0-a/halal_db"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define models using SQLAlchemy's declarative_base
Base = declarative_base()

# Create the Metadata Object
metadata_obj = MetaData()

# Creating tables 
products = Table(
    'products', metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('product_name', String(255)),
    Column('product_description', String(255)),
    Column('product_img', String(255)),
    Column('halal_status', Integer, ForeignKey('halal_status.id')),
    Column('subcategory_id', Integer, ForeignKey('subcategories.id')),
    Column('cis', String(255))
)

halal_status = Table(
    'halal_status', metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String(255))
)

category = Table(
    'categories', metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('img_url', String(255))
)

subcategory = Table(
    'subcategories', metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('img_url', String(255)),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

# To create all above listed tables in database
metadata_obj.create_all(engine)

