<div align="center">

  # 🖥️ AGAC API

  <sub>The **anime-girls-and-computers** API!</sub>

</div>

This is an API for anime-girls-and-computers [github repo](https://github.com/THEGOLDENPRO/anime-girls-and-computers).

## 🌐 Publicly available instances
| Country | URL | Hosted by | Notes |
|:-----------:|:-------:|:-------------:|:---------:|
| 🇩🇪 | https://api.ananas.moe/agac/v1 | [r3tr0ananas](https://github.com/r3tr0ananas) | Official Instance |
| 🇺🇸 | https://api.emretech.gay/agac | [EmreTech](https://github.com/EmreTech) | Instance hosted with help from Ananas |

## 🛠️ Self-Host
How to host your own AGAC API instance

### 🐬 Docker Method (recommended)
1. Pull the image
```sh
docker pull r3tr0ananas/agac-api:latest
``` 
2. Then launch a container with this command.
> *you don't really need to mount a volume but it's recommended*
```sh
docker run -p 8000:8000/tcp -v ./cached_images:/app/assets/cache r3tr0ananas/agac-api:latest
```
3. Now visit ``localhost:8000`` in your browser and there you go! 👍
> *if you wanna use docker-compose, [this file](./docker-compose.yml) might be useful to you*

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
4. Pull the ~~anime girls~~ images.
```sh
make get-repo
```
5. Run.
```sh
make run
```
6. Visit ``localhost:8083`` in your browser, then all should be good! 🌈
