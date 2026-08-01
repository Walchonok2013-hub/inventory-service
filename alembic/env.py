
import os
import sys
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# 1. Получаем конфиг Alembic
config = context.config

# 2. КРИТИЧЕСКИ ВАЖНО: Читаем переменную окружения и сразу перезаписываем URL в конфиге
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)
    print(f"DEBUG: Alembic successfully loaded DATABASE_URL from env.")
else:
    # Если переменной нет, миграция упадет сразу с понятной ошибкой, а не позже
    raise RuntimeError("Ошибка: Переменная окружения DATABASE_URL не найдена! Проверьте docker-compose.yml")

# 3. Настраиваем логирование (используя уже обновленный конфиг)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 4. Добавляем корень проекта в sys.path, чтобы Python видел твои модели
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 5. Импортируем модели (только после добавления пути!)
from app.models.base import Base
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()