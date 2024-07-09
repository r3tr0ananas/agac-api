import sys
sys.path.insert(0, ".")

import os
from api import __version__

build_name = "r3tr0ananas/agac-api"

os.system(
    f"docker build -t {build_name}:{__version__} --build-arg ARCH=amd64 ."
)

os.system(
    f"docker build -t {build_name}:latest --build-arg ARCH=amd64 ."
)