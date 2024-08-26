build: get-repo install

install:
	pip install . -U

run:
	fastapi dev api/main.py

get-repo:
	git clone https://github.com/THEGOLDENPRO/anime-girls-and-computers ./assets/repo