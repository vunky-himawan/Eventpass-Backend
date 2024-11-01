from fastapi import FastAPI
from .interface.api.routes import user_routes
from .infrastructure.config.database import Base, engine
from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Hapus semua tabel
    Base.metadata.drop_all(bind=engine)  
    # Buat semua tabel lagi
    Base.metadata.create_all(bind=engine)  
    print("Database initialized")
    yield  # Titik di mana aplikasi berjalan
    print("Shutting down application...")

app = FastAPI(title="Eventpass API", version="1.0.0", lifespan=lifespan)

# Include routers
app.include_router(user_routes, prefix="/api/v1", tags=["Users"])