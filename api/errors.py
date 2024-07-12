from fastapi import Request
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from pydantic import BaseModel

__all__ = (
    "CategoryNotFound",
    "ImageNotFound",
    "ImageMetadataNotFound",
)

class CategoryNotFound(BaseModel):
    error: str
    message: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "CategoryNotFound",
                    "message": "The category 'ubuntu' was not found!"
                }
            ]
        }
    }

class ImageNotFound(BaseModel):
    error: str
    message: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "ImageNotFound",
                    "message": "We couldn't find a image with search id 'nanami_aoyama_arch'!"
                }
            ]
        }
    }

class ImageMetadataNotFound(BaseModel):
    error: str
    message: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "ImageMetadataNotFound",
                    "message": "We couldn't find a image's metadata with search id 'nanami_aoyama_arch'!"
                }
            ]
        }
    }

class RateLimited(BaseModel):
    error: str
    message: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "RateLimited",
                    "message": "Rate limit exceeded: 3 per 1 second (Follow the rates: https://github.com/r3tr0ananas/agac-api/wiki#-rate-limiting)"
                }
            ]
        }
    }

def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    response = JSONResponse(
        status_code = 429,
        content = {
            "error": "RateLimited", 
            "message": f"Rate limit exceeded: {exc.detail} (Follow the rates: https://github.com/r3tr0ananas/agac-api/wiki#-rate-limiting)"
        }
    )

    response = request.app.state.limiter._inject_headers(
        response, request.state.view_rate_limit
    )

    return response