from django.conf.urls import url
from foo import views
urlpatterns = [
    url(r'^execute/', views.execute, name='execute'),
    url(r'^create/', views.create, name='create'),
    url(r'^generate/', views.generate, name='generate'),
    url(r'^collect/', views.collect, name='collect'),
    url(r'^command/(?P<action>[a-z]+)/$', views.command, name='command'),
    url(r'^command/(?P<action>[a-z]+)/(?P<category>[a-z]+)/(?P<operation>[a-z]+)/$', views.command, name='command'),
]