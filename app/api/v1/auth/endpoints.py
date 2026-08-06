from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse 
from app.core.database import get_db
from app.models.user import User
from pydantic import BaseModel
from app.api.v1.auth.password import get_password_hash, verify_password
from app.api.v1.auth.jwt import create_access_token
from app.api.v1.auth.password import verify_password
# Убрали OAuth2PasswordRequestForm — он больше не нужен

auth_router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


@auth_router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Хеширование пароля
    hashed_password = get_password_hash(user_data.password)

    # Создание пользователя
    db_user = User(username=user_data.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@auth_router.post("/login")
def login_for_access_token(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    username = login_data.username
    password = login_data.password

    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}