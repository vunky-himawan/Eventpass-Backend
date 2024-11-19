# from fastapi import FastAPI
# import importlib
# import os
# import sys
#
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#
# from interface.http.api.routes.auth.authentication_routes import router as authentication_routes, get_login_usecase
# from dotenv import load_dotenv
#
# load_dotenv()
#
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# routes_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), 'interface/http/api/routes/'))
# sys.path.append(routes_directory)
#
# app = FastAPI(title="Eventpass API", version="1.0.0")
#
# api_version = "v1"
#
# def include_all_routers(app: FastAPI, base_path: str, prefix: str = ""):
#     for root, _, files in os.walk(base_path):
#         for file in files:
#             if file.endswith(".py") and not file.startswith("__"):
#                 # Compute the module's import path
#                 relative_path = os.path.relpath(os.path.join(root, file), base_path)
#                 module_name = relative_path.replace(os.sep, ".").rsplit(".py", 1)[0]
#
#                 # Import the module
#                 module = importlib.import_module(module_name)
#
#                 # Check if the module defines a router
#                 if hasattr(module, "router"):
#                     app.include_router(module.router, prefix=f"/api/{prefix}/{module_name.split('.')[-1]}", tags=[module_name.split('.')[-1]])
#
# def include_all_routers(app: FastAPI, base_path: str, base_package: str, prefix: str = ""):
#     """
#     Dynamically discover and include all routers from the given base path.
#
#     :param app: FastAPI application instance
#     :param base_path: The base directory path to search for route modules
#     :param base_package: The base Python package corresponding to the base path
#     :param prefix: URL prefix for the routes
#     """
#     for root, _, files in os.walk(base_path):
#         for file in files:
#             if file.endswith(".py") and file != "__init__.py":
#                 # Compute the module path
#                 relative_path = os.path.relpath(root, base_path)
#                 module_name = (
#                     f"{base_package}.{relative_path.replace(os.sep, '.')}.{file[:-3]}"
#                 )
#
#                 try:
#                     # Import the module
#                     module = importlib.import_module(module_name)
#
#                     # Include the router if it exists
#                     if hasattr(module, "router"):
#                         app.include_router(
#                             getattr(module, "router"), prefix=prefix, tags=[module_name.split('.')[-1]]
#                         )
#                         print(f"Included router from: {module_name}")
#                 except Exception as e:
#                     print(f"Failed to include router from {module_name}: {e}")
#
# # Include routers
# # app.include_router(authentication_routes, prefix="/api/v1/auth", tags=["Authentication"])
# include_all_routers(app, routes_directory, prefix=api_version)

from fastapi import FastAPI
import os
import sys
import importlib.util
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Eventpass API", version="1.0.0")

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

