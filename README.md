# Docker Foresight

```
pip install poetry==1.7.1
poetry install --sync
```

```
$ poetry run docker_foresight --file Dockerfile

Score: 13.76
1: FROM python:3.10.12-slim
2: WORKDIR /app/
14: COPY pyproject.toml pyproject.toml | <--- Change rate of 1.83
16: COPY .gitignore README.md /app | <--- Change rate of 3.67
```

TODO Add threshold pass/fail for CICD:
```
THRESHOLD=13
$ poetry run docker_foresight --file Dockerfile --threshold $THRESHOLD
Score: 13.76
Expected: 13
FAILURE
$ echo $?
1
```
