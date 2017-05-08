import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proxypool.settings")
django.setup()

import threading

from myproxy.fetch import crwal
from myproxy.SortDt import sort
from myproxy.VerifyProxy import verify

TASKS = [crwal,sort,verify]

def handle_tasks():

    threads = []
    for i in TASKS:
        p = threading.Thread(target=i)
        threads.append(p)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


handle_tasks()
a = input()

