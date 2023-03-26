from aiohttp import web
from app.api import crud

async def create_user(request: web.Request) -> web.Response:
    data = await request.json()
    name = data.get("name")

    if not name:
        return web.Response(status=400, text="Name is required")

    user = await crud.crud_create_user(name)

    return web.json_response(
        {
            "id": user.id,
            "name": user.name,
            "balance": user.balance,
        },
        status=201,
    )

async def get_user_balance(request: web.Request) -> web.Response:
    id = int(request.match_info["id"])
    date = request.query.get("date")

    try:
        balance = await crud.crud_get_user_balance(id, date)
    except ValueError as e:
        return web.Response(status=404, text=str(e))

    return web.json_response({"balance": balance}, status=200)

async def get_user_balance(request: web.Request) -> web.Response:
    id = int(request.match_info["id"])
    date = request.query.get("date")

    try:
        balance = await crud.crud_get_user_balance(id, date)
    except ValueError as e:
        return web.Response(status=404, text=str(e))

    return web.json_response({"balance": balance}, status=200)


async def add_transaction(request: web.Request) -> web.Response:
    data = await request.json()
    uid = data.get("uid")
    txn_type = data.get("type")
    amount = float(data.get("amount"))
    user_id = data.get("user_id")
    timestamp = data.get("timestamp")

    try:
        transaction = await crud.crud_add_transaction(
            uid, txn_type, amount, user_id, timestamp
        )
    except ValueError as e:
        return web.Response(status=402, text=str(e))

    return web.json_response(
        {
            "id": transaction.id,
            "amount": transaction.amount,
        },
        status=200,
    )

async def get_transaction(request: web.Request) -> web.Response:
    uid = request.match_info["uid"]

    try:
        transaction = await crud.crud_get_transaction(uid)
    except ValueError as e:
        return web.Response(status=400, text=str(e))

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
