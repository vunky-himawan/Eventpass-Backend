from fastapi import FastAPI
from .interface.http.api.routes.test_routes import router as test
from .interface.http.api.routes.user_routes import router as user_routes
from .interface.http.api.routes.authentication.authentication_routes import router as authentication_routes
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Eventpass API", version="1.0.0")

# Include routers
# app.include_router(test, prefix="/api/v1", tags=["Test"])
app.include_router(authentication_routes, prefix="/api/v1/auth", tags=["Authentication"])
# app.include_router(user_routes, prefix="/api/v1", tags=["Users"])