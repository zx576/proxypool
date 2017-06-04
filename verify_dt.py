# coding=utf-8
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proxypool.settings")
django.setup()


from myproxy.VerifyProxy import verify


verify()