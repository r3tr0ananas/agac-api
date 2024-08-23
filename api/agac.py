from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Union, List, Dict

from pathlib import Path

import random
import subprocess

from .image import Image
from .constants import GIT_PATH, ALLOWED_FILE_EXTENSIONS

__all__ = ("Agac",)

class Agac:
    """A class for interfacing with the AGAC TOML Files."""
    def __init__(self) -> None:
        self._repo_path = Path(GIT_PATH)

        self.head_commit = self.__update_repo()
        self.images, self.categories = self.__phrase_images()
    
    def get_random(self, category: str = None) -> Image:
        if category is not None:
            if category in self.categories:
                return random.choice(self.categories[category])
        
        return random.choice(self.images)
    
    def get(self, id: str) -> Optional[Image]:
        for image in self.images:
            if image.id == id:
                return image

        return None
            
    def __update_repo(self):
        print(
            f"Pulling agac repo '{self._repo_path}'..."
        )

        process = subprocess.Popen(
            ["git", "pull"],
            text = True, 
            stdout = subprocess.PIPE, 
            cwd = self._repo_path
        )

        process.wait()
        output, _ = process.communicate()

        if not process.returncode == 0:
            print(f"ERROR: {output}")

        hash_process = subprocess.Popen(
            ["git", "rev-parse", "HEAD"], 
            text = True, 
            stdout = subprocess.PIPE, 
            cwd = self._repo_path
        )

        hash_process.wait()
        hash, _ = hash_process.communicate()

        return hash.replace("\n", "")

    def __phrase_images(self) -> Union[List[Image], Dict[str, List[Image]]]:
        images = []
        categories = {}

        for index, file in enumerate(self._repo_path.rglob("*")):

            if file.suffix not in ALLOWED_FILE_EXTENSIONS:
                continue
            
            image = Image(
                path = file
            )

            images.append(image)
            image_categories = str(file).split("/")[2:-1]       

            for category in image_categories:
                if category not in categories:
                    categories[category] = []

                categories[category].append(image)  

        return images, dict(sorted(categories.items()))