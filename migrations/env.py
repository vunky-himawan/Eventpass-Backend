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

# Import the base class from the models (usually where your Base metadata is defined)
from src.infrastructure.config.database import Base  # Update this import if your Base class is defined elsewhere

# Automatically import all modules in the models directory
def import_models(models_directory):
    for filename in os.listdir(models_directory):
        if filename.endswith(".py") and filename != "__init__.py":
            # Module name with package context (use dots instead of slashes)
            module_name = filename[:-3]  # Remove '.py' from the filename to get module name
            module_path = f"src.infrastructure.database.models.{module_name}"
            try:
                importlib.import_module(module_path)  # Correctly import the module
            except ModuleNotFoundError as e:
                print(f"Module {module_path} could not be imported: {e}")

# Run the model import function to load all models
import_models(models_directory)

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

