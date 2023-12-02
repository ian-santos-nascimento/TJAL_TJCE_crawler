from . import views
from django.urls import path
urlpatterns = [
    path('', views.ApiProcessView.as_view(), name="Api")
]