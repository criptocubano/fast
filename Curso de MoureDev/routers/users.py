from  fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router=APIRouter()

class User(BaseModel):
    id : int
    name: str
    surname: str
    
    age: int
    

user_lists=[User(id=1, name="Carlos", surname="Vargas", age=34),
           User(id=2, name="Juan", surname="Peres", age=14),
           User(id=3, name="Auron", surname="P34eres", age=134)
           ]

@router.get("/")
async def root():   
    return "Hola mundo "


@router.get("/users/")
async def users():
    return user_lists

@router.get("/user/{id}")
async def user(id:int):
    return search_user(id)
    
@router.post("/user/" , status_code=201)
async def user(user:User):
    print(user)
    if type(search_user(user.id))==User:
        
        raise HTTPException(status_code=404, detail="fue mal brooo") #el codigo de fastapi se adapta
        
    else:
        user_lists.append(user)
        print(user_lists)
        return {"Success"}


@router.put("/user/" )
async def user_json(user:User):
    
    found= False
    
    for index,save_user in enumerate(user_lists):
        if save_user.id == user.id:
            user_lists[index]=user            
            found=True
            
    if not found:
        return {"error": "No se ha actualizado el usuario"}
    
    return user

@router.delete("/user/{id}")
async def user(id:int):
    
    found= False
    
    for index,save_user in enumerate(user_lists):
        if save_user.id == id:
            del user_lists[index]
            found=True
            return {"eiminado con exito"}
            
    if not found:
        return {"error": "No se ha eliminado el  el usuario"}

    
def search_user(id:int):
    users =filter(lambda user: user.id ==id, user_lists)
    try:
        return list(users)[0]
    except:
        return {"error" : "No se ah encontrado el usuario"} 