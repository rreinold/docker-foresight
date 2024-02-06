# Docker Foresight

```
pip install poetry==1.7.1
poetry install --sync
```

```
$ poetry run docker_foresight --file Dockerfile
Score: 103.18
        1   : FROM python:3.10.12-slim
        2   : WORKDIR /app/
        18  : ENV PYTHONUNBUFFERED=1
        19  : ENV POETRY_CACHE_DIR=/tmp/pypoetry
        22  : RUN apt-get update && apt-get install --no-install-recommends gcc=4:12.2.0-3 -y && rm -rf /var/lib/apt/lists/*
        24  : RUN pip --no-cache-dir install poetry==1.6.1
HIGH    26  : COPY pyproject.toml poetry.lock ./
        31  : RUN poetry install --with sql --without dev --no-root --no-directory
HIGH    33  : COPY README.md README.md
HIGH    34  : COPY great_expectations_cloud great_expectations_cloud
LOW     35  : COPY examples/agent/data data
        37  : RUN poetry install --only-root && rm -rf POETRY_CACHE_DIR
        39  : ENTRYPOINT ["poetry", "run", "gx-agent"]
```

Using threshold for pass/fail:
```
THRESHOLD=13
$ poetry run docker_foresight --file Dockerfile --threshold $THRESHOLD
Score: 13.76
Expected: 13
FAILURE
$ echo $?
1
```
