from django.contrib import admin
from .models import Proxy

# admin.site.register(Proxy)
@admin.register(Proxy)
class ProxyAdmin(admin.ModelAdmin):

    date_hierarchy = 'created_time'
    list_filter = ('status','resourse','created_time')
    # max_elements = len(Proxy.objects.all())
    # list_max_show_all = max_elements
    list_per_page = 50
    # pass

# Register your models here.
