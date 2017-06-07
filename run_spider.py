import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proxypool.settings")
django.setup()

from myproxy.utils.fetch import crwal


if __name__ == '__main__':
    crwal()
