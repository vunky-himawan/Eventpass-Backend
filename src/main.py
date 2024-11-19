from fastapi import FastAPI
import os
import sys
import importlib.util
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

app = FastAPI(title="Eventpass API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_version = "v1"

# Define the routes directory relative to the current file
routes_directory = os.path.join(os.path.dirname(__file__), "interface", "http", "api", "routes")

# Function to load routers dynamically
def load_routes(directory: str, app: FastAPI, api_version: str):
    for root, _, files in os.walk(directory):
        for file in files:
            if file == "main.py":  # Target only `main.py` files
                module_path = os.path.join(root, file)
                
                # Get the parent folder name for the prefix
                last_folder = os.path.basename(os.path.dirname(module_path))
                
                # Convert path to a module import string
                relative_path = os.path.relpath(module_path, os.path.dirname(__file__))
                module_name = relative_path.replace(os.sep, ".").removesuffix(".py")
                
                # Import the module
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                
                # Check if the module has a `router` attribute
                if hasattr(module, "router"):
                    prefix = f"/api/{api_version}/{last_folder}"  # Add prefix based on the last folder
                    # Include the router with its prefix
                    app.include_router(module.router, prefix=prefix, tags=[last_folder.capitalize().replace("_", " ")])

# Load all routes
load_routes(routes_directory, app, api_version)