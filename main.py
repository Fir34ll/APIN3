from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import models, schemas
from datetime import datetime
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "API EM FUNCIONAMENTO"}

@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(**item.dict())
    db_item.current_bid = item.starting_bid
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.post("/buyers/", response_model=schemas.Buyer)
def create_buyer(buyer: schemas.BuyerCreate, db: Session = Depends(get_db)):
    db_buyer = models.Buyer(**buyer.dict())
    db.add(db_buyer)
    db.commit()
    db.refresh(db_buyer)
    return db_buyer

@app.post("/bids/", response_model=schemas.Bid)
def create_bid(bid: schemas.BidCreate, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == bid.item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if datetime.fromisoformat(item.auction_end_time) < datetime.now():
        raise HTTPException(status_code=400, detail="Auction has ended")
    if bid.amount <= item.current_bid:
        raise HTTPException(status_code=400, detail="Bid amount must be greater than current bid")
    item.current_bid = bid.amount
    db_bid = models.Bid(**bid.dict())
    db.add(db_bid)
    db.commit()
    db.refresh(db_bid)
    db.refresh(item)
    return db_bid

@app.get("/items/", response_model=list[schemas.Item])
def list_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()

@app.get("/items/{item_id}", response_model=schemas.Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
