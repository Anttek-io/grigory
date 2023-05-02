FROM python:3.10-alpine as base

ENV PYTHONUNBUFFERED 1
ENV PATH="/venv/bin:$PATH"

RUN addgroup -S -g 1000 django && \
    adduser -S -G django -u 999 django && \
    apk add --no-cache curl

WORKDIR /home/django


FROM base as requirements

COPY requirements.txt .

RUN python -m venv /venv && \
    . /venv/bin/activate && \
    pip install --no-cache-dir -U setuptools && \
    pip install --no-cache-dir -r requirements.txt


FROM base as source-code

COPY . .

RUN rm -fr requirements.txt


FROM base

COPY --from=requirements /venv /venv

USER django

COPY --from=source-code --chown=django:django /home/django /home/django

RUN chmod +x /home/django/entrypoint.sh

ENTRYPOINT ["/home/django/entrypoint.sh"]

CMD ["gunicorn"]

EXPOSE 8000
