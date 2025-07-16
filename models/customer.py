from sqlalchemy import Column,Integer,String
from database import Base,SessionLocal

class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(Integer,primary_key=True)
    name = Column(String(100))
    email = Column(String(100),unique=True)
    phone_no = Column(String(30))
    location = Column(String(100))


    
