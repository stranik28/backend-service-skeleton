from gino import Gino
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

db = Gino()

class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    balance = Column(Float, default=0)

    transactions = relationship("Transaction", back_populates="user")

    @validates('balance')
    def validate_balance(self, value):
        if value < 0:
            raise ValueError("Balance can't be negative.")
        return value
    


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    type = Column(String, nullable=False)
    date = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    uid = Column(String, nullable=False, index=True)
    user = relationship("User", back_populates="transactions")
