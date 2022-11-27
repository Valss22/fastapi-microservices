from pydantic import BaseModel


class Price(BaseModel):
    amount: float
    currency: str


class Item(BaseModel):
    price: Price
