from fastapi import FastAPI
from app.schemas.user import UserCreate, UserResponse


app = FastAPI(title="Users API")



@app.get("/")
def root():
    return {"message": "Users API funcionando"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    return {
        "id": 1,
        "nombre": user.nombre,
        "apellido": user.apellido,
        "username": user.username,
        "email": user.email,
        "avatar": user.avatar,
        "rol": user.rol,
        "estado": True
    }