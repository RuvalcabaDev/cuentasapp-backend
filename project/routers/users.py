from typing import List
from typing import Optional
from fastapi import Cookie
from fastapi import Response
from fastapi import Depends
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials

from ..database import User

from ..schemas import UserRequestModel
from ..schemas import UserResponseModel
from ..schemas import ReviewResponseModel

from ..common import get_current_user

from ..Connections import ConnectionMySQL

router = APIRouter(prefix='/users')
database_connection = ConnectionMySQL()


@router.post('')
async def create_user(user: UserRequestModel):
    query = "SELECT username FROM users WHERE username = %s;"
    print("COMENZANDO A CREAR USUARIO")
    database_connection.mysql_connect()
    user_exists = database_connection.cursor.execute(query, (user.username))
    print("Usuario existe:", user_exists, sep=" --- ")
    database_connection.connection.commit()
    database_connection.mysql_close()
    if user_exists != 0:
        raise HTTPException(409, 'El username ya se encuentra en uso.')
    hash_password = User.create_password(user.password)
    user = User(
        username=user.username,
        password=hash_password
    )
    try:
        query = 'INSERT INTO users(username, password) VALUES(%s, %s);'
        print("El usuario no existe, creando nuevo usuario")
        database_connection.mysql_connect()
        database_connection.cursor.execute(query, (user.username, user.password))
        database_connection.connection.commit()
        print("Usuario nuevo creado:", user.username, sep=" --- ")
        database_connection.mysql_close()
    except Exception as e:
        print("Ocurrió una excepción:", e, sep=" --- ")
    return {"message": f"Bienvenido {user.username}"}


@router.post('/login', response_model=UserResponseModel)
async def login(credentials: HTTPBasicCredentials, response: Response):
    user = User.select().where(User.username == credentials.username).first()

    if user is None:
        raise HTTPException(404, 'User not found')

    if user.password != User.create_password(credentials.password):
        raise HTTPException(404, 'Password error')

    response.set_cookie(key='user_id', value=user.id)  # TOKEN

    return user


@router.get('/reviews', response_model=List[ReviewResponseModel])
async def get_reviews(user: str = Depends(get_current_user)):
    return [user_review for user_review in user.reviews]
