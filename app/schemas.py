from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str
    starting_bid: float
    auction_end_time: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    current_bid: float

    class Config:
        from_attributes = True

class BuyerBase(BaseModel):
    name: str

class BuyerCreate(BuyerBase):
    pass

class Buyer(BuyerBase):
    id: int

    class Config:
        from_attributes = True

class BidBase(BaseModel):
    item_id: int
    buyer_id: int
    amount: float

class BidCreate(BidBase):
    pass

class Bid(BidBase):
    id: int

    class Config:
        from_attributes = True
