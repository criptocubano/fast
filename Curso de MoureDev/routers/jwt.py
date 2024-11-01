from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm # para capturar el usuario y la contrasena
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
ALGORITHM="HS256"
ACCESS_TOKEN_DURATION=1

oauth2=OAuth2PasswordBearer(tokenUrl='login')

crypt = CryptContext(schemes=["bcrypt"])




app=FastAPI()
class User(BaseModel):
    username: str
    name: str
    email: str
    disabled : bool


class UserDB(User):
    password: str

users_db={
    'carlosdev':{
        "username": "carlosdev",
        "name":"Carlos",
        "email": "maure@uci.cu",
        "disabled" : False,
        "password": "$2a$12$37cuMKtwHYtbw1txIhVrfeORvvhqrCmdAGoTwE20HO47dGUOnxc2y"
    
    },
    'mouredev2':{
        "username": "carlosdev2",
        "name":"Carlos2",
        "email": "maure@uci.cu2",
        "disabled" : True,
        "password": "$2a$12$O66lX6PMFQpatvWnP9ALH.FABhlXpL2kn6VHVVPGJ5m2GT98YHbjm"
    
    },
    "mouredev":{
        "username": "carlosdev3",
        "name":"Carlos",
        "email": "maure@uci.cu",
        "disabled" : False,
        "password": "$2a$12$O66lX6PMFQpatvWnP9ALH.FABhlXpL2kn6VHVVPGJ5m2GT98YHbjm"
    
    }
    
}

def search_user(username: str): 
    if username in users_db:
        return UserDB(**users_db[username])

async  def current_user(user:User = Depends(oauth2)):
    user=search_user(token)
    if not user : 
        raise HTTPException(status_code=401,  
                            detail="Credenciales de autenticacion invalidos")
    return user #




@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db= users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")
    user=search_user(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail="La contrasena no es correcta")
        
    return {"access_token":user.password, "token_type": "bearer"} #

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db= users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")
    
    user=search_user(form.username)
    
    
        
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="La contrasena no es correcta")

    
    
    access_token={"sub": user.username ,
                 "exp":datetime.utcnow() + 
                 timedelta(minutes=ACCESS_TOKEN_DURATION)}
    
    return {"access_token":jwt.decode(access_token,algorithms=ALGORITHM) ,"token_type": "bearer"} #


@app.get("/users/me")
async def me(user:User=Depends(current_user)):
    return user