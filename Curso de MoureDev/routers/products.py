from  fastapi import APIRouter

router=APIRouter()



@router.get("/products")
async def productos():
    return ["Producto 1","Producto 2","Producto 3", "Producto 4"]