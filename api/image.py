from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List

from typing_extensions import TypedDict, final

from pathlib import Path
from dataclasses import dataclass, field
from fastapi.responses import FileResponse, StreamingResponse
import toml
from PIL import Image as PImage
import io

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
        self.authors = self.toml.get("authors", [])
        self.category = str(self.path).split("/")[3]
        self.tags = self.toml.get("tags", [])
        self.sources = self.toml.get("sources", [])


    def to_dict(self) -> ImageData:
        return {
            "id": self.id,
            "name": self.name,
            "authors": self.authors,
            "category": self.category,
            "tags": self.tags,
            "sources": self.sources
        }

    def to_file_response(self, raw: bool = False) -> FileResponse:
        """Returns file response object."""
        if raw is False:
            image = PImage.open(self.path)

            if image.size[0] >= 3840 and image.size[1] >= 2160:
                image = image.resize((1920, 1080))

            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)

            return StreamingResponse(
                img_byte_arr, 
                media_type="image/png",
                headers = {
                    "Expires": "0",
                    "x-image-id": self.id
                }
            )

        return FileResponse(
            self.path,
            headers = {
                "Expires": "0",
                "x-image-id": self.id
            }
        )