# coding=utf-8
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proxypool.settings")
django.setup()


from myproxy.utils.SortDt import sort


if __name__ == '__main__':
    sort()

