import os

import psycopg
from dotenv import load_dotenv
from pwdlib import PasswordHash


load_dotenv()

password_hash = PasswordHash.recommended()




def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def get_users():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, nombre, apellido, username, email, avatar, rol, estado
                FROM usuarios
                ORDER BY id
                """
            )

            return cursor.fetchall()

def get_user(user_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, nombre, apellido, username, email, avatar, rol, estado
                FROM usuarios
                WHERE id = %s
                """,
                (user_id,),
            )

            return cursor.fetchone()

def verify_password(password, hashed_password):
    return password_hash.verify(password, hashed_password)

def get_user_by_email(email):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    nombre,
                    apellido,
                    username,
                    email,
                    password,
                    avatar,
                    rol,
                    estado
                FROM usuarios
                WHERE email = %s
                """,
                (email,),
            )

            return cursor.fetchone()


def create_user(user):
    hashed_password = password_hash.hash(user.password)
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO usuarios (
                    nombre,
                    apellido,
                    username,
                    email,
                    password,
                    avatar,
                    rol
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    user.nombre,
                    user.apellido,
                    user.username,
                    user.email,
                    hashed_password,
                    user.avatar,
                    user.rol.value,
                ),
            )

            return cursor.fetchone()[0]


def update_user(user_id, user):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE usuarios
                SET
                    nombre = %s,
                    apellido = %s,
                    username = %s,
                    email = %s,
                    avatar = %s,
                    rol = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING id
                """,
                (
                    user.nombre,
                    user.apellido,
                    user.username,
                    user.email,
                    user.avatar,
                    user.rol.value,
                    user_id,
                ),
            )

            return cursor.fetchone()


def delete_user(user_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM usuarios
                WHERE id = %s
                RETURNING id
                """,
                (user_id,),
            )

            return cursor.fetchone()