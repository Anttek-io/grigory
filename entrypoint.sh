#!/bin/bash

python manage.py migrate --noinput || exit 1
if [[ "$DJANGO_DEBUG" -eq "False" || "$COLLECT_STATIC" -eq "True" ]]; then
    python manage.py collectstatic --noinput || exit 1
fi
exec "$@"
