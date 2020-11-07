from django.urls import path

from catalog import views
from catalog.views import test_view

urlpatterns = [
    path('', views.index, name = 'index')
]
