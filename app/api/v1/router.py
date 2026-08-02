from fastapi import APIRouter

from app.api.v1.auth.endpoints import auth_router
from app.api.v1.users import router as users_router

# Создаем общий роутер для версии API v1
api_router = APIRouter()

# Подключаем роутер авторизации с префиксом /auth
# Итоговый путь будет: /api/v1/auth/...
api_router.include_router(auth_router, prefix="/auth")

# Подключаем роутер пользователей (без дополнительного префикса, если он уже есть внутри users.py)
# Итоговый путь будет: /api/v1/users/...
api_router.include_router(users_router, prefix="/users")

# Если позже добавишь товары, раскомментируй и добавь аналогично:
# from app.api.v1.items.endpoints import items_router
# api_router.include_router(items_router, prefix="/items")