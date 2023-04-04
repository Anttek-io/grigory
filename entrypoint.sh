#!/bin/sh

python manage.py migrate --noinput || exit 1
if [ "$DJANGO_DEBUG" = "False" ]; then
    python manage.py collectstatic --noinput || exit 1
fi
exec "$@"
