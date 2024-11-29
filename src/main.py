from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
import sys
import importlib.util
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from src.utils.symlink import create_symlinks

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

def create_static_folder():
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

def create_uploads_folder():
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)

static_dir = os.path.join('..', os.getenv("STATIC_DIR", "dist"))
uploads_dir = os.path.join('..', os.getenv("UPLOADS_DIR", "uploads"))

create_static_folder()
create_uploads_folder()

create_symlinks(os.getenv("UPLOADS_DIR", "uploads"), os.getenv("STATIC_DIR", "dist"), "static", os.getenv("UPLOADS_DIR", "uploads"))

app = FastAPI(title="Eventpass API", version="1.0.0")

app.mount("/static", StaticFiles(directory=os.getenv("STATIC_DIR", "dist"),follow_symlink=True), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_version = "v1"
routes_directory = os.path.join(os.path.dirname(__file__), "interface", "http", "api", "routes")

def load_routes(directory: str, app: FastAPI, api_version: str):
    for root, _, files in os.walk(directory):
        for file in files:
            if file == "main.py":
                module_path = os.path.join(root, file)
                last_folder = os.path.basename(os.path.dirname(module_path))
                
                relative_path = os.path.relpath(module_path, os.path.dirname(__file__))
                module_name = relative_path.replace(os.sep, ".").removesuffix(".py")
                
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                
                if hasattr(module, "router"):
                    prefix = f"/api/{api_version}/{last_folder}"
                    app.include_router(module.router, prefix=prefix, tags=[last_folder.capitalize().replace("_", " ")])

load_routes(routes_directory, app, api_version)
