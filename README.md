# Docker Foresight

```
pip install poetry==1.7.1
poetry install --sync
```

```
poetry run docker_foresight --file Dockerfile
1: FROM python:3.10.12-slim
2: WORKDIR /app/
14: COPY pyproject.toml pyproject.toml | <--- Change rate of 0.15
16: COPY .gitignore README.md /app | <--- Change rate of 0.23
```
