from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .database import UserReview
from .routers import user_router
from .routers import review_router
from .common import create_access_token

from .database import User
from .database import Movie
from .Connections import ConnectionMySQL

app = FastAPI(title='CuentasApp API',
              description='Proyecto backend API CuentasApp',
              version='1.0')

api_v1 = APIRouter(prefix='/api/v1')

api_v1.include_router(user_router)
api_v1.include_router(review_router)
app.include_router(api_v1)
database_connection = ConnectionMySQL()


@app.post('/auth')
async def auth(data: OAuth2PasswordRequestForm = Depends()):
    user = User.authenticate(data.username, data.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        'access_token': create_access_token(user[0], user[1]),
        'token_type': 'bearer'
    }


@app.on_event("startup")
async def startup():
    print("Inicio del servicio")


@app.on_event("shutdown")
async def startup():
    database_connection.mysql_close()
    print("La conexión se apagó")
