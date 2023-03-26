from app.models import User
from app.models import db
from app.models import Transaction
from datetime import datetime

async def date_to_timestamp(date: str) -> int:
    return datetime.strptime(date[:23],'%Y-%m-%dT%H:%M:%S.%f' \
                            if '.' in date[:23] else '%Y-%m-%dT%H:%M:%S')

async def create_user(name: str) -> User:
    result = await User.create(name=name)
    return result

async def get_user(id: int) -> User:
    result = await User.get(id)
    if result is None:
        raise ValueError('User not found')
    return result

async def get_user_balance(id: int, date: str = None) -> User:
    result = await get_user(id)
    if date is None:
        return result.balance
    date = await date_to_timestamp(date)
    query = db.select([db.func.sum(db.case([
        (Transaction.type == 'DEPOSIT', Transaction.amount),
        (Transaction.type == 'WITHDRAW', -Transaction.amount)
    ], else_=0)).label('balance')]).where(
        (Transaction.user_id == id) & (Transaction.date <= date)
    )
    return await db.scalar(query)


async def add_transaction(
        uid: str, txn_type: str, amount: float, user_id: int, timestamp: str) -> Transaction:

    if txn_type not in ['DEPOSIT', 'WITHDRAW']:
        raise ValueError('Transaction type must be DEPOSIT or WITHDRAW')
    
    if txn_type == 'WITHDRAW':
        balance = await get_user_balance(user_id)
        if balance < amount:
            raise ValueError('Not enough money to withdraw')
        
    timestamp = await date_to_timestamp(timestamp)

    result = await Transaction.create(uid=uid, type=txn_type, amount=amount,    
                                        user_id=user_id, date=timestamp)
    
    amount = -amount if txn_type == 'WITHDRAW' else amount

    await User.update.values(balance=User.balance + amount).where(User.id == user_id).gino.status()

    return result

async def get_transaction(uid: str) -> Transaction:
    result = await Transaction.query.where(Transaction.uid == uid).gino.first()
    if result is None:
        raise ValueError('Transaction not found')
    return result