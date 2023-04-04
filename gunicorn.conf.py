# Gunicorn configuration file
# https://docs.gunicorn.org/en/stable/configure.html#configuration-file
# https://docs.gunicorn.org/en/stable/settings.html
import multiprocessing

wsgi_app = 'core.asgi:application'

log_level = 'info'

accesslog = '-'

workers = multiprocessing.cpu_count() + 1

threads = 2 * multiprocessing.cpu_count()

bind = '0.0.0.0:8000'

timeout = 600

preload = True

worker_class = 'core.asgi.UvicornWorker'
