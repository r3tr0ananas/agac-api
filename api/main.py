from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import os

from . import __version__

ROOT_PATH = (lambda x: x if x is not None else "")(os.environ.get("ROOT_PATH"))

app = FastAPI(
    title = "api", 
    description = "", 
    license_info = {
        "name": "", 
        "identifier": "",
    }, 
    swagger_favicon_url = "", 
    version = f"v{__version__}",

    root_path = ROOT_PATH
)

@app.get("/")
async def root(request: Request):
    return "Hello World"
