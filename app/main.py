from fastapi import FastAPI
from app.api.v1.auth.endpoints import auth_router

# app = FastAPI(
#     title="Inventory Service API",
#     description="API для управления инвентарем и пользователями",
#     version="1.0.0"
# )
app = FastAPI(debug=True)
# ✅ ЭТО ЕДИНСТВЕННОЕ подключение роутера, которое должно быть в main.py
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])

@app.get("/")
def read_root():
    return {"status": "ok", "message": "API is running"}

