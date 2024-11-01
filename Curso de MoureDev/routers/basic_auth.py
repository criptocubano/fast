from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm # para capturar el usuario y la contrasena

oauth2=OAuth2PasswordBearer(tokenUrl='login')

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
        "password": "123456"
    
    },
    'mouredev2':{
        "username": "carlosdev2",
        "name":"Carlos2",
        "email": "maure@uci.cu2",
        "disabled" : True,
        "password": "1234562"
    
    },
    "mouredev":{
        "username": "carlosdev3",
        "name":"Carlos",
        "email": "maure@uci.cu",
        "disabled" : False,
        "password": "123456"
    
    }
    
}

@app.get("/")
async def root():
    return {"message": "Hello World"}


def search_user(username: str): 
    if username in users_db:
        return UserDB(**users_db[username])

async  def current_user(token : str = Depends(oauth2)):
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


@app.get("/users/me")
async def me(user:User=Depends(current_user)):
    return user