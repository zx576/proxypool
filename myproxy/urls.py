from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.index,name='index'),

    url(r'^manage/$',views.manage,name='manage'),

    url(r'verify/$',views.verify,name='verify'),
    # url(r'stopverify/$',views.stop_verify,name='stop_verify'),

    url(r'get/$',views.get,name='get'),

    url(r'work/$',views.work,name='work'),
    # url(r'stopcrwal/$',views.stop_crwal,name='stopcrwal'),

    url(r'sort/$',views.sort,name='sort'),

    url(r'chart/$',views.chart,name='chart'),
    url(r'api-ins/$',views.api_ins,name='api'),

    # url(r'login/$',views.login_,name='login'),
    # url(r'register/$',views.register_,name = 'register'),

    url(r'req/$',views.judge_request,name='req')
    #temp
    # url(r'clear/$',views.clear,name='clear')
]
