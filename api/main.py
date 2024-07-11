from typing import List, Tuple

from fastapi import FastAPI
from fastapi.responses import RedirectResponse, JSONResponse, FileResponse
from fastapi.requests import Request

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from thefuzz import fuzz
from urllib.parse import unquote
from os import environ

from .agac import Agac
from .image import Image, ImageData
from .constants import RATE_LIMIT
from . import __version__, errors

ROOT_PATH = (lambda x: x if x is not None else "")(environ.get("ROOT_PATH"))

limiter = Limiter(key_func=get_remote_address, headers_enabled = True)
app = FastAPI(
    title = "AGAC-API",
    description = "", 
    license_info = {
        "name": "MIT", 
        "identifier": "MIT",
    }, 
    version = f"v{__version__}",

    root_path = ROOT_PATH
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, errors.rate_limit_handler)

agac = Agac()

@app.get("/")
async def root(request: Request):
    return RedirectResponse(f"{ROOT_PATH}/docs")

@app.get(
    "/info",
    name = "Info about the current instance.",
    tags = ["other"]
)
async def info():
    """Returns repository information like image count and etc."""
    return {
        "version": __version__, 
        "image_count": len(agac.images)
    }

@app.get(
    "/get/{id}",
    name = "Allows you to get a image by search id.",
    tags = ["image"],   
    response_class = FileResponse,
    responses = {
        200: {
            "content": {
                "image/png": {},
                "image/jpeg": {}
            },
            "description": "Returned an image successfully. 😁",
        },
        404: {
            "model": errors.ImageNotFound,
            "description": "The image was not Found."
        },
    },
)
@limiter.limit(f"{RATE_LIMIT}/second")
async def get(request: Request, id: str, raw: bool = False):
    image = agac.get(id)

    if image is not None:
        return image.to_file_response(raw)
    
    return JSONResponse(
        status_code = 404, 
        content = {
            "error": "ImageNotFound",
            "message": f"We couldn't find a image with id '{id}'!"
        }
    )

@app.get(
    "/get/{id}/metadata",
    name = "Allows you to get a image's metadata by search id.",
    tags = ["image"],
    response_class = JSONResponse,
    responses = {
        200: {
            "model": ImageData,
            "description": "Returned an image's metadata successfully. 😁",
        },
        404: {
            "model": errors.ImageMetadataNotFound,
            "description": "The image's metadata was not Found."
        },
    },
)
async def get_metadata(request: Request, id: str):
    image = agac.get(id)

    if image is not None:
        return image.to_dict()
    
    return JSONResponse(
        status_code = 404, 
        content = {
            "error": "ImageNotFound",
            "message": f"We couldn't find a image with id '{id}'!"
        }
    )

@app.get(
    "/random",
    name = "Get a random image",
    tags = ["image"],
    response_class = FileResponse,
    responses = {
        200: {
            "content": {
                "image/png": {},
                "image/jpeg": {}
            },
            "description": "Returned an image successfully. 😁",
        },
    },
)
@limiter.limit(f"{RATE_LIMIT}/second")  
async def random_image(request: Request, category: str = None, raw: bool = False):
    image = agac.get_random(category)

    return image.to_file_response(raw)

@app.get(
    "/search",
    name = "Query for images.",
    tags = ["image"],
    response_class = JSONResponse,
    responses = {
        200: {
            "model": List[ImageData],
            "description": "Returns list of image objects.",
        },
    },
)
async def search(
    request: Request, 
    query: str,
    category: str = None,
    limit: int = 10
):
    images: List[Tuple[int, Image]] = []

    for image in agac.images:
        if len(images) == limit:
            break

        if category is not None and not category.lower() == image.category.lower():
            continue

        name_match = fuzz.partial_ratio(image.name.lower(), unquote(query.lower()))

        if name_match > 70:
            images.append((name_match, image))

    images.sort(key = lambda x: x[0], reverse = True) # Sort in order of highest match.

    return [
        image[1].to_dict() for image in images
    ]

@app.get(
    "/categories",
    name = "All Available Categories",
    tags = ["image"],
    response_class = JSONResponse,
    responses = {
        200: {
            "description": "Returns a list of all available categories.",
        },
    },
)
async def categories(request: Request):
    return list(agac.categories.keys())     


