from django.contrib import admin
from .models import Proxy, IpAddr

@admin.register(Proxy)
class ProxyAdmin(admin.ModelAdmin):

    date_hierarchy = 'created_time'
    list_filter = ('status','resourse','created_time')
    list_per_page = 50


@admin.register(IpAddr)
class IpAddrAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_time'
    list_per_page = 50
