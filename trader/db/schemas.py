from typing import Optional
from pydantic import BaseModel


class AssetBase(BaseModel):
    name: str
    symbol: str
    price: float


class AssetCreate(AssetBase):
    pass


class AssetUpdate(AssetBase):
    id: int


class AssetSchema(AssetBase):
    id: int

    class Config:
        orm_mode = True


class TradeBase(BaseModel):
    asset_id: int
    type: str
    price: float
    quantity: float


class TradeCreate(TradeBase):
    pass


class TradeUpdate(TradeBase):
    id: int


class TradeSchema(TradeBase):
    id: int
    created_at: Optional[str]

    class Config:
        orm_mode = True
