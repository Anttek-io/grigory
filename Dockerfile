# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-alpine as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

ARG USER=django
ARG WORKDIR=/app
WORKDIR ${WORKDIR}

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
# Add curl to base image to support health checks.
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "${WORKDIR}" \
    --shell "/sbin/nologin" \
    --uid "${UID}" \
    ${USER} && \
    apk add --no-cache curl

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER ${USER}

# Copy the source code into the container.
COPY . .

# Set custom shell script as entrypoint of container.
ENV WORKDIR=${WORKDIR}
ENTRYPOINT "${WORKDIR}/entrypoint.sh"

# Expose the port that the application listens on.
EXPOSE 8000
