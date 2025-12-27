from sqlalchemy import Column, Integer, String, Float, Boolean
from ..database import Base  # Relative import

class Phone(Base):
    __tablename__ = "phones"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    brand = Column(String, index=True, nullable=False)
    ram = Column(String)
    storage = Column(String)
    cpu = Column(String)
    screen = Column(String)
    battery = Column(String)
    os = Column(String)
    price = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    final_price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    warranty = Column(String)
    image_url = Column(String, default="")
    is_active = Column(Boolean, default=True)