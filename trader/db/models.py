from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    symbol = Column(String, unique=True, index=True)
    price = Column(Float, nullable=False)
    trades = relationship("Trade", back_populates="asset")


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    type = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())

    asset = relationship("Asset", back_populates="trades")
