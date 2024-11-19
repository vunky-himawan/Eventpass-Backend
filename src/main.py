from fastapi import FastAPI
import os
import sys
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interface.http.api.routes.authentication.authentication_routes import router as authentication_routes, get_login_usecase
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Eventpass API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(authentication_routes, prefix="/api/v1/auth", tags=["Authentication"])
