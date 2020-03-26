from django.conf.urls import url
from calculator import views

urlpatterns = [
    url('solve', views.solve),
]
