from django.conf.urls import url
from gaming import views

urlpatterns = [
    url('generate', views.generate),
    # url('challenge', views.Poly2View.as_view()),
]
