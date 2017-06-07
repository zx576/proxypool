from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^manage/$',views.manage,name='manage'),
    url(r'get/$',views.get,name='get'),
    url(r'work/$',views.work,name='work'),
    url(r'chart/$',views.chart,name='chart'),
    url(r'api-ins/$',views.api_ins,name='api'),
    url(r'req/$',views.judge_request,name='req')
]
