# coding=utf-8
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proxypool.settings")
django.setup()

from myproxy.models import Proxy

invalid = Proxy.objects.filter(status='I')

invalid.delete()