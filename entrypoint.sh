#!/bin/sh

python manage.py migrate --noinput || exit 1
if [ "$DJANGO_DEBUG" = "False"  ] || [ "$DJANGO_COLLECT_STATIC" = "True" ]; then
  python manage.py collectstatic --noinput || exit 1
fi
exec gunicorn "$@"
