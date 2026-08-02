from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Импорты задач и БД
from app.tasks import process_inventory_update, simple_add
from app.core.database import get_db

# Импорты моделей и схем
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

# Утилиты
from app.api.v1.auth.password import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])
@router.get("/")
def get_users():
    return [{"id": 1, "name": "Test"}]
@router.post("/trigger-task")
def trigger_task():
    """
    Отправляет задачи в очередь Celery.
    Возвращает ID задач для отслеживания статуса (AsyncResult).
    """
    try:
        # 1. Запускаем простую задачу для проверки связи
        task_simple = simple_add.delay(10, 20)
        
        # 2. Раскомментируй эту строку, когда будешь готов тестировать реальную логику
        # task_inventory = process_inventory_update.delay(item_id=123, new_quantity=50)
        
        return {
            "message": "Задачи успешно отправлены в очередь Redis!",
            "simple_add_task_id": task_simple.id,
            # "inventory_task_id": task_inventory.id
        }
    
    except Exception as e:
        # Если Redis упал или Celery не отвечает, мы не должны молча падать.
        # Лучше вернуть понятную ошибку клиенту.
        logger.error(f"Не удалось отправить задачу в очередь: {e}")
        raise HTTPException(
            status_code=503, 
            detail="Не удалось отправить задачу в очередь. Проверьте сервисы Redis и Celery."
        )

@router.post("/", response_model=UserResponse)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # Проверка на уникальность username ИЛИ email
    existing_user = db.query(User).filter(
        (User.username == user_in.username) | (User.email == user_in.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="Username or email already registered"
        )

    # Хеширование пароля
    hashed_password = get_password_hash(user_in.password)
    
    # Создание пользователя
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user