from django.conf.urls import url
from calculator.views import solve

urlpatterns = [
    url('solve', solve),
]
