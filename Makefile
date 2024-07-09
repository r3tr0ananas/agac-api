build: get-repo install

install:
	pip install . -U

run:
	uvicorn api.main:app --reload --port 8083

get-repo:
	git clone https://github.com/THEGOLDENPRO/anime-girls-and-computers ./assets/repo