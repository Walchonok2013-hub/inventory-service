import logging
from sqlalchemy.orm import Session
from celery.exceptions import Retry

# Абсолютный импорт от корня проекта (важно для Docker)
from app.core.database import SessionLocal

from .celery import celery_app

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def process_inventory_update(self, item_id: int, new_quantity: int):
    db: Session | None = None  # Объявляем переменную ДО блока try
    
    try:
        # Создаём новую сессию именно здесь
        db = SessionLocal()
        logger.info(f"[Worker] Начинаю обработку товара ID={item_id}. Сессия создана.")

        # --- ТВОЯ БИЗНЕС-ЛОГИКА ---
        # from app.models import Item
        # item = db.query(Item).filter(Item.id == item_id).first()
        # if item:
        #     item.quantity = new_quantity
        #     db.commit()
        #     logger.info(f"[Worker] Товар обновлён в БД.")
        
        logger.info(f"[Worker] Эмуляция записи в БД для товара {item_id}... Готово.")
        return {"status": "success", "item_id": item_id, "quantity": new_quantity}

    except Exception as exc:
        logger.error(f"[Worker] Произошла ошибка: {exc}")
        
        try:
            raise self.retry(exc=exc)
        except self.MaxRetriesExceededError:
            logger.critical(f"[Worker] Все попытки исчерпаны. Ошибка: {exc}")
            if db is not None:
                db.rollback()
            raise

    finally:
        # Гарантированно закрываем сессию
        if db is not None:
            db.close()
            logger.debug("[Worker] Сессия БД закрыта.")

@celery_app.task
def simple_add(x: int, y: int) -> int:
    result = x + y
    logger.info(f"Выполнено сложение: {x} + {y} = {result}")
    return result