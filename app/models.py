from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    starting_bid = Column(Float)
    current_bid = Column(Float, default=0.0)
    auction_end_time = Column(String)  

    bids = relationship("Bid", back_populates="item")

class Buyer(Base):
    __tablename__ = "buyers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    bids = relationship("Bid", back_populates="buyer")

class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    buyer_id = Column(Integer, ForeignKey("buyers.id"))
    amount = Column(Float)

    item = relationship("Item", back_populates="bids")
    buyer = relationship("Buyer", back_populates="bids")
