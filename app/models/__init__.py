from gino import Gino
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

db = Gino()

class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    balance = Column(Float, default=0)

    transactions = relationship("Transaction", back_populates="user")
    


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    type = Column(String, nullable=False)
    date = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    uid = Column(String, nullable=False, index=True)
    user = relationship("User", back_populates="transactions")
