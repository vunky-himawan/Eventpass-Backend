import os
import sys
import importlib
from logging.config import fileConfig
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from alembic import context
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the models directory to the sys path for dynamic imports
models_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), './../src/infrastructure/database/models'))
sys.path.append(models_directory)

# Import the base class from the models (ensure only one correct import)
from src.infrastructure.config.database import Base  # Correct the import if needed

# Dynamically import models to avoid circular dependencies
model_modules = [
    'user', 'participant', 'face_photos', 'transaction', 'ticket', 'feedback_rating',
    'event_organizer', 'event', 'speaker', 'event_speaker', 
    'organization_member', 'notification', 'attendance'
]

for model in model_modules:
    importlib.import_module(f"src.infrastructure.database.models.{model}")

# Set target_metadata to Base.metadata to support autogeneration
target_metadata = Base.metadata

# Alembic Config object to access the .ini file
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    url = url.replace("${DB_USER}", os.getenv("DB_USER"))
    url = url.replace("${DB_PASSWORD}", os.getenv("DB_PASSWORD"))
    url = url.replace("${DB_HOST}", os.getenv("DB_HOST"))
    url = url.replace("${DB_NAME}", os.getenv("DB_NAME"))

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    url = config.get_main_option("sqlalchemy.url")
    url = url.replace("${DB_USER}", os.getenv("DB_USER"))
    url = url.replace("${DB_PASSWORD}", os.getenv("DB_PASSWORD"))
    url = url.replace("${DB_HOST}", os.getenv("DB_HOST"))
    url = url.replace("${DB_NAME}", os.getenv("DB_NAME"))

    connectable = create_engine(url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

