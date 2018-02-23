from django.conf.urls import url
from foo import views
urlpatterns = [
    url(r'^execute/', views.execute, name='execute'),
    url(r'^generate/', views.generate, name='generate'),
    url(r'^command/', views.command, name='command'),
]