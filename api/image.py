from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List

from typing_extensions import TypedDict, final

from pathlib import Path
from dataclasses import dataclass, field
from fastapi.responses import FileResponse
from PIL import Image as PImage

import toml

from .constants import CACHE_PATH

__all__ = (
    "ImageData",
    "Image",
)

@final
class AuthorsData(TypedDict):
    name: str
    github: str

@final
class ImageData(TypedDict):
    id: str
    name: str
    authors: List[AuthorsData]
    category: str
    tags: List[str]
    sources: List[str]

@dataclass
class Image:
    path: Path = field(repr=False)  

    id: str = field(default=None)
    name: str = field(default=None)
    authors: str = field(default=None)
    category: str = field(default=None)
    tags: List[str] = field(default=None)
    sources: List[str] = field(default=None)

    def __post_init__(self):
        self.toml_path = self.path.parent.joinpath(self.path.stem + ".toml")
        self.toml = toml.loads(self.toml_path.read_text()).get("metadata", {})

        self.id = self.path.stem
        self.name = self.toml.get("name", "")
        self.authors = self.toml.get("authors", []) or [self.toml.get("author", [])]
        self.category = str(self.path).split("/")[3]
        self.tags = self.toml.get("tags", [])
        self.sources = self.toml.get("sources", [])
    
    def downscale_image(self) -> Path:
        downscaled_image_path = Path(CACHE_PATH).joinpath(self.path.stem + ".webp")

        if downscaled_image_path.exists():
            return downscaled_image_path

        image = PImage.open(self.path)

        image.save(downscaled_image_path, format="WEBP")

        return downscaled_image_path

    def to_dict(self) -> ImageData:
        return {
            "id": self.id,
            "name": self.name,
            "authors": self.authors,
            "category": self.category,
            "tags": self.tags,
            "sources": self.sources
        }

    def to_file_response(self, raw: bool = False, expire: str = "300") -> FileResponse:
        """Returns file response object."""
        if raw is False:
            downscaled_image = self.downscale_image()

            return FileResponse(
                downscaled_image,
                media_type="image/webp",
                headers = {
                    "Expires": expire,
                    "x-image-id": self.id
                }
            )

        return FileResponse(
            self.path,
            headers = {
                "Expires": expire,
                "x-image-id": self.id
            }   
        )