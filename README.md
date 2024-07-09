<div align="center">

  # 🖥️ AGAC API

  <sub>Behold the **anime-girls-and-computers** API!</sub>

</div>

This is an API for anime-girls-and-computers [github repo](https://github.com/THEGOLDENPRO/anime-girls-and-computers).

## 🌐 Publicly available instances
- Coming Soon™

## 🛠️ Self-Host
How to host your own AGAC API instance

### 🐬 Docker Method (recommended)
Coming Soon™

### 🐍 Native Method (recommended for development)

#### Prerequisites:
- [Git](https://git-scm.com/downloads)
- [Python](https://www.python.org/downloads/) (3.8 - 3.11)
- [Make](https://www.gnu.org/software/make/#download) ***(otherwise you'll have to copy the commands from the [Makefile](https://github.com/r3tr0ananas/agac-api/blob/main/Makefile))***

1. Clone the repo.
```sh
git clone https://github.com/r3tr0ananas/agac-api && cd agac-api
```
2. Create env.
```sh
python -m venv env
source env/bin/activate # For windows it's --> cd env/Scripts && activate && cd ../../
```
3. Install the API's dependencies.
```sh
make
```
4. Pull the ~~anime girls~~ computer images.
```sh
make get-repo
```
5. Run that sh#t.
```sh
make run
```
6. Visit ``localhost:8003`` in your browser, then all should be good! 🌈
