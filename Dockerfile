FROM python:3.10-slim-bullseye as base


FROM base as builder

COPY requirements.txt .

RUN python -m venv /venv && \
    source /venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt


FROM base

COPY --from=builder /venv /venv

ENV PATH="/venv/bin:$PATH"

ENV PYTHONUNBUFFERED 1

ARG CACHE_DATE=not_a_date

RUN echo $CACHE_DATE

COPY . .

RUN chmod +x /home/django/entrypoint.sh

ENTRYPOINT ["/home/django/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000
