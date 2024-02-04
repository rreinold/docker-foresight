FROM python:3.10.12-slim
WORKDIR /app/

# File Structure:
#
# /app
# ├── great_expectations_cloud/
# │         ├── agent/
# │         └── ...
# ├── pyproject.toml
# ├── poetry.lock
# └── README.md

COPY pyproject.toml pyproject.toml

COPY .gitignore README.md /app
