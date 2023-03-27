from aiohttp import web
import app.api.crud as crud


async def create_user(request: web.Request) -> web.Response:
    '''
        Создание пользователя на вход принимает 
        name:str
    '''
    data = await request.json()
    name = data.get("name")

    if not name:
        raise web.HTTPBadRequest(text="Name is required")

    user = await crud.create_user(name)

    return web.json_response(
        {
            "id": user.id,
            "name": user.name,
            "balance": user.balance,
        },
        status=201,
    )

async def get_user_balance(request: web.Request) -> web.Response:
    '''
        Получение баланса пользователя, входные данные
        id:int
        date:timestamp[Optional]
    '''
    id = int(request.match_info["id"])
    date = request.query.get("date")

    try:
        balance = await crud.get_user_balance(id, date)
    except ValueError as e:
        raise web.HTTPNotFound(text=str(e))

    return web.json_response({"balance": balance}, status=200)

async def add_transaction(request: web.Request) -> web.Response:
    '''
        Добавление транзакции, на вход подаются данные:
        uid:UID
        type: Enum('DEPOSIT', 'WITHDRAW')
        amount:float
        user_id:int
        timestamp:timestamp

    '''
    data = await request.json()
    uid = data.get("uid")
    txn_type = data.get("type")
    amount = float(data.get("amount"))
    user_id = data.get("user_id")
    timestamp = data.get("timestamp")

    try:
        transaction = await crud.add_transaction(
            uid, txn_type, amount, user_id, timestamp
        )
    except ValueError as e:
        raise web.HTTPPaymentRequired(text=str(e))

    return web.json_response(
        {
            "id": transaction.id,
            "amount": transaction.amount,
        },
        status=200,
    )

async def get_transaction(request: web.Request) -> web.Response:
    '''
        Получение тразакци, на вход подается
        uid:UID
    '''
    uid = request.match_info["uid"]

    try:
        transaction = await crud.get_transaction(uid)
    except ValueError as e:
        raise web.HTTPBadRequest(text=str(e))

    return web.json_response(
        {
            "id": transaction.id,
            "amount": transaction.amount,
            "type": transaction.type,
            "date": str(transaction.date),
            "user_id": transaction.user_id,
            "uid": transaction.uid,
        },
        status=200,
    )


def add_routes(app):
    app.router.add_route('POST', r'/v1/user', create_user, name='create_user')
    app.router.add_route('GET', r'/v1/user/{id}', get_user_balance, name='get_user')
    app.router.add_route('POST', r'/v1/transaction', add_transaction, name='add_transaction')
    app.router.add_route('GET', r'/v1/transaction/{uid}', get_transaction, name='incoming_transaction')