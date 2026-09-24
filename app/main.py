from fastapi import FastAPI, HTTPException, status

from app.database import create_user, get_users, get_user, update_user, delete_user, get_user_by_email, verify_password
from app.schemas.user import UserCreate, UserResponse, UserUpdate, LoginRequest


app = FastAPI(title="Users API")


@app.get("/")
def root():
    return {"message": "Users API funcionando"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/users", response_model=UserResponse)
def create_user_endpoint(user: UserCreate):
    user_id = create_user(user)

    return {
        "id": user_id,
        "nombre": user.nombre,
        "apellido": user.apellido,
        "username": user.username,
        "email": user.email,
        "avatar": user.avatar,
        "rol": user.rol,
        "estado": True,
    }

@app.get("/users", response_model=list[UserResponse])
def list_users():
    users = get_users()

    return [
        {
            "id": user[0],
            "nombre": user[1],
            "apellido": user[2],
            "username": user[3],
            "email": user[4],
            "avatar": user[5],
            "rol": user[6],
            "estado": user[7],
        }
        for user in users
    ]

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user_endpoint(user_id: int):
    user = get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return {
        "id": user[0],
        "nombre": user[1],
        "apellido": user[2],
        "username": user[3],
        "email": user[4],
        "avatar": user[5],
        "rol": user[6],
        "estado": user[7],
    }


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user_endpoint(user_id: int, user: UserUpdate):

    updated_user = update_user(user_id, user)

    if updated_user is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    updated_user = get_user(user_id)

    return {
        "id": updated_user[0],
        "nombre": updated_user[1],
        "apellido": updated_user[2],
        "username": updated_user[3],
        "email": updated_user[4],
        "avatar": updated_user[5],
        "rol": updated_user[6],
        "estado": updated_user[7],
    }

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id:int):
    deleted_user= delete_user(user_id)

    if deleted_user is None:
        raise HTTPException(
            status_code= 404,
            detail="Usuario no encontrado"
        )

    return None

@app.post("/login")
def login(login_data: LoginRequest):

    user = get_user_by_email(login_data.email)
    
    if user is None:
        raise HTTPException(
            status_code = 404,
            detail = "Credenciales invalidas"
        )

    if not user[8]:
        raise HTTPException(
            status_code=403,
            detail="Usuario deshabilitado"
        )

    
    password_valid = verify_password(
        login_data.password,
        user[5]
    )

    if not password_valid:
        raise HTTPException(
            status_code = 404,
            detail = "Credenciales invalidas"
        )
    
    return {
        "message": "Login exitoso",
        "user_id": user [0],
        "email": user[4],
        "rol": user [7]

    }