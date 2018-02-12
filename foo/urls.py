from django.conf.urls import url
from foo import views
urlpatterns = [
    url(r'^execute/', views.execute, name='execute'),
]