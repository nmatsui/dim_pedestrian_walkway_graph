FROM python:3.10-slim as builder
WORKDIR /opt
RUN apt update && apt upgrade -y && \
    pip install -U pip poetry
COPY src/pyproject.toml src/poetry.lock ./
RUN poetry export -f requirements.txt > requirements.txt

FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /opt
COPY --from=builder /opt/requirements.txt .
RUN apt update && apt upgrade -y && \
    pip install -U pip && pip install -r requirements.txt
COPY src ./src
ENTRYPOINT ["/opt/src/main.py"]
