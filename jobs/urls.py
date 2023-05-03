from django.urls import path
from django.urls import re_path as url 
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
#from jobs.views import 
from jobs.views import (CategoryListAPIView,SubcategoryListview,CategoryWebListAPIView)
router = DefaultRouter()
urlpatterns = [
    path('', include(router.urls)), 
    path('cats/',CategoryListAPIView.as_view(), name='cats-list'),
    path('webcats/',CategoryWebListAPIView.as_view(), name='cats-list'),
    url(r'^cats/(?P<id>[0-9]+)/subcats/$', SubcategoryListview.as_view(), name='sub category'),
]