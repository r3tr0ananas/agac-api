from decouple import config

__all__ = (
    "GIT_PATH",
    "GIT_REPO_URL",
    "CACHE_PATH",
    "ALLOWED_FILE_EXTENSIONS",
    "RATE_LIMIT"
)

ALLOWED_FILE_EXTENSIONS = [".png", ".jpeg", ".jpg", ".webp"]
GIT_PATH = config("GIT_PATH", default = "./assets/repo", cast = str)
CACHE_PATH = config("CACHE_PATH", default = "./assets/cache", cast = str)
GIT_REPO_URL = config("GIT_REPO_URL", default = "https://github.com/THEGOLDENPRO/anime-girls-and-computers", cast = str)
RATE_LIMIT = config("RATE_LIMIT", default = 3, cast = int)