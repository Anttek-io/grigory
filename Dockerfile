FROM python:3.10-slim-bullseye as base

SHELL ["/bin/bash", "-c"]


FROM base as builder

COPY requirements.txt .

RUN python -m venv /venv && \
    source /venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt


FROM base

WORKDIR /home/django

COPY --from=builder /venv /venv

ENV PATH="/venv/bin:$PATH"

ENV PYTHONUNBUFFERED 1

COPY . .

RUN chmod +x /home/django/entrypoint.sh

ENTRYPOINT ["/home/django/entrypoint.sh"]

CMD ["uvicorn", "core.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--reload", "--lifespan", "off"]

EXPOSE 8000
