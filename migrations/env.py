import os
import sys
from dotenv import load_dotenv

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# Add src to path
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
sys.path.append(project_path)

print("Project Path:", project_path)
print("Updated sys.path:", sys.path)

# Load environment variables
load_dotenv()

# Import models
from infrastructure.config.database import Base
from infrastructure.database.models.user import UserModel
from infrastructure.database.models.participant import ParticipantModel
from infrastructure.database.models.face_embeddings import FaceEmbeddingModel
from infrastructure.database.models.transaction import TransactionModel
from infrastructure.database.models.ticket import TicketModel
from infrastructure.database.models.feedback_rating import FeedbackRatingModel
from infrastructure.database.models.event_organizer import EventOrganizerModel
from infrastructure.database.models.event import EventModel
from infrastructure.database.models.speaker import SpeakerModel
from infrastructure.database.models.organization_member import OrganizationMemberModel
from infrastructure.database.models.event_employee import EventEmployeeModel
from infrastructure.database.models.event_detail import EventDetailModel
from infrastructure.database.models.notification import NotificationModel
from infrastructure.database.models.attendance import AttendanceModel

target_metadata = Base.metadata

# Get DB URL from environment
config = context.config
DB_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
config.set_main_option("sqlalchemy.url", DB_URL)

target_metadata = Base.metadata

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
