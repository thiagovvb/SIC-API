# from django.conf.urls import url
from django.urls import path, include
from .views import (
    InfoAppealApiView,
    ListInfoRequestApiView,
    InfoRequestApiView
)

urlpatterns = [
    path('list', ListInfoRequestApiView.as_view()),
    path('info-request', InfoRequestApiView.as_view()),
    path('info-appeal', InfoAppealApiView.as_view())
]