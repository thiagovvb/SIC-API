# from django.conf.urls import url
from django.urls import path, include
from .views import (
    ListInfoRequestApiView,
)

urlpatterns = [
    path('list', ListInfoRequestApiView.as_view())
]