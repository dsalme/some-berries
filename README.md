## How to run
This app includes a Dockerfile and a docker-compose file, which are used to spin up a FastAPI http server in a docker container.
Docker compose takes care of mapping a container's port to a host's port so that you can access the api locally.

##### If you don't have docker, you can install it by **[following these instructions](https://docs.docker.com/engine/install/)**

In order to start the app, you need to run:
```bash
cp .env.example .env
```

### Build docker image
```bash
docker compose build
```

### Start docker container
```bash
docker compose up
```

### How to hit the app's API
This will start the app and expose it through the `8000` port.
(you can select a different port in the `ports` section inside the docker-compose.yaml file, for example `8001:8000` will map port 8001 in the host to port 8000 in the container)
You can hit the api through a web browser navigating to:
```
localhost:8000
```
or using `curl` in your terminal:
```bash
curl localhost:8000
```

### In case you want to run it outside the docker container

In order to run the app outside docker, you'll need to set up/install a couple of dependencies:

#### Python

##### If you don't have python, you can install it by **[following these instructions](https://www.python.org/downloads/)**

#### UV
I'm using `uv` as a python dependency manager and python's virtual env manager.

##### How to install

You can follow the instructions here: https://github.com/astral-sh/uv?tab=readme-ov-file#installation
TLDR:
```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# With pip.
pip install uv
# Or pipx.
pipx install uv
```

Once `uv` is installed, sync dependencies (install dependencies in uv's virtual env):

```bash
uv venv # creates a virtual env
uv lock # creates a lock file
uv sync # installs dependencies in virtual env
```

Then you can:
```bash
uv run uvicorn berries:app --host 0.0.0.0 --port 8000 --env-file .env
```


## How to run tests:
Dev dependencies include pytest, you can run tests by running this in your terminal, which will run tests inside the container:
```bash
docker compose exec berries uv run pytest
```
Or outside the container:
```bash
uv run --env-file .env -- pytest
```
