from logging.config import fileConfig
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, engine_from_config
from sqlalchemy import pool

import importlib
import pkgutil
from infrastructure.database import models

from infrastructure.config.database import Base

from alembic import context

load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

imported_models = {}
for _, module_name, _ in pkgutil.iter_modules(models.__path__):
    full_module_name = f"infrastructure.database.models.{module_name}"
    module = importlib.import_module(full_module_name)

    # Iterate through all attributes of the module
    for attribute_name in dir(module):
        # Check if the attribute is a class and its name contains 'Model'
        if "Model" in attribute_name:
            attribute = getattr(module, attribute_name)
            if isinstance(attribute, type):  # Ensure it's a class
                imported_models[attribute_name] = attribute

# Print imported models
for model_name, model_class in imported_models.items():
    print(f"Imported: {model_name} from {model_class.__module__}")

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    url = config.get_main_option("sqlalchemy.url")
    url = url.replace("${DB_USER}", os.getenv("DB_USER"))
    url = url.replace("${DB_PASSWORD}", os.getenv("DB_PASSWORD"))
    url = url.replace("${DB_HOST}", os.getenv("DB_HOST"))
    url = url.replace("${DB_NAME}", os.getenv("DB_NAME"))

    connectable = create_engine(url)

    # connectable = engine_from_config(
    #     config.get_section(config.config_ini_section, {}),
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )

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
