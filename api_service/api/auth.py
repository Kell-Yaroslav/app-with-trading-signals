"""Эндпоинты аутентификации: регистрация и логин."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud
from app.models import User
from api_service.auth.jwt import create_access_token
from api_service.auth.password import hash_password, verify_password
from api_service.dependencies import get_session
from api_service.schemas.user import UserCreate, UserRead
from api_service.schemas.token import Token


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    session: Session = Depends(get_session),
):
    """
    Регистрация нового пользователя.

    - Проверяет, что username и email уникальны
    - Хеширует пароль
    - Создаёт пользователя с ролью trader по умолчанию
    - Возвращает данные пользователя (без пароля)
    """
    # Проверка уникальности username
    if crud.get_user_by_username(session, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким username уже существует",
        )

    # Проверка уникальности email
    existing = session.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует",
        )

    # Роль trader по умолчанию (первый зарегистрированный может стать админом, если нужно)
    trader_role = crud.get_role_by_name(session, "trader")
    if not trader_role:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Роль trader не найдена. Запустите seed.py",
        )

    # Хешируем пароль
    password_hash = hash_password(user_data.password)

    # Создаём пользователя
    user = crud.create_user(
        session=session,
        username=user_data.username,
        email=user_data.email,
        password_hash=password_hash,
        role_id=trader_role.id,
    )

    return user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    """
    Логин пользователя.

    Принимает form-data: username, password.
    Возвращает: JWT-токен.
    """
    # Ищем пользователя по username
    user = crud.get_user_by_username(session, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Проверяем пароль
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Проверяем, что пользователь активен
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь заблокирован",
        )

    # Создаём JWT-токен
    access_token = create_access_token(
        data={
            "sub": user.username,
            "user_id": user.id,
            "role": user.role.name,
        }
    )

    return Token(access_token=access_token, token_type="bearer")