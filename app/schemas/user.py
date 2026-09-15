from enum import Enum

from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    admin = "admin"
    editor = "editor"
    usuario = "usuario"


class UserCreate(BaseModel):
    nombre: str
    apellido: str
    username: str
    email: EmailStr
    password: str
    avatar: str | None = None
    rol: UserRole = UserRole.usuario


class UserResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    username: str
    email: EmailStr
    avatar: str | None = None
    rol: UserRole
    estado: bool