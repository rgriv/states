from django.conf.urls import url

from . import views

app_name = 'states'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^display/$', views.display, name = "display")
]
