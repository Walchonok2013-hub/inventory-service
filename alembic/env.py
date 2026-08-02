import os
import sys
from pathlib import Path
from app.models.base import Base
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent  # Это /app
core_package_path = project_root / "app"   # Это /app/app

if str(core_package_path) not in sys.path:
    sys.path.insert(0, str(core_package_path))

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from core.config import settings
from app.models import Base

# Получаем URL базы данных из настроек проекта
config = context.config

# Подключаем файл логов alembic.ini, если он есть
if config.config_file_name:
    fileConfig(config.config_file_name)

# Указываем Alembic, какие таблицы нужно отслеживать (все модели из app.models)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Запускает миграции в офлайн-режиме (без прямого подключения к БД)."""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Запускает миграции в онлайн-режиме (с реальным подключением к БД)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        # Переопределяем URL подключения на тот, что в .env (чтобы работало в Docker)
        url=settings.DATABASE_URL,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()