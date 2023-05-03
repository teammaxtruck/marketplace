from django.urls import path
from django.urls import re_path as url 
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from proprety.views import (CategoryListAPIView,SubcategoryListview,PropretyListAPIView,HomeApropretyAPIView,
                            MyPropretyAPIView,PropFavoritApiView,MyPropretyRejectApiView,MyPropretyPendingApiView,
                          MyPropretyDisActiveApiView, MyPropretyActiveApiView, ImagesListAPIView,
                          SearchKeywordAPIVIEW,SearchFilterAPIVIEW,CategoryWebListAPIView,CatpropretyAPIView)

router = DefaultRouter()
urlpatterns = [
    path('', include(router.urls)), 
    path('cats/',CategoryListAPIView.as_view(), name='cats-list'),
    path('webcats/',CategoryWebListAPIView.as_view(), name='cats-list'),
    url(r'^cats/(?P<id>[0-9]+)/subcats/$', SubcategoryListview.as_view(), name='sub category'),
    path('proprety/add/',PropretyListAPIView.as_view(), name='proprety-post '), #post
    path('proprety/view/<int:prop_id>', PropretyListAPIView.as_view(), name='proprety-view'), #get
    path('proprety/home/<str:prop_type>',HomeApropretyAPIView.as_view(),name='Sael - Rent - All Home'), #get
    path('proprety/cat/<int:cat_id>',CatpropretyAPIView.as_view(),name='cat'), #get

    
       #get
    path('proprety/update/<int:auto_id>',PropretyListAPIView.as_view(), name='proprety-update '),
        #put 
    path('proprety/delete/<int:auto_id>',PropretyListAPIView.as_view(), name='proprety-delete '),
        #delete 
    path('proprety/active/<int:auto_id>', PropretyListAPIView.as_view(), name='proprety-Active_Upadte'),
        #patch
    path('proprety/myprop/',MyPropretyAPIView.as_view(),name='my proprety'), # get
    path('proprety/fav/',PropFavoritApiView.as_view(),name='favorit'), #post
    path('proprety/myfav/',PropFavoritApiView.as_view(),name='my favorit'), # get
    path('proprety/myproprety/active/',MyPropretyActiveApiView.as_view(),name='Active'), 
    path('proprety/myproprety/disactive/',MyPropretyDisActiveApiView.as_view(),name=' Dis active'), 
    path('proprety/myproprety/reject/',MyPropretyRejectApiView.as_view(),name=' reject'), 
    path('proprety/myproprety/pending/',MyPropretyPendingApiView.as_view(),name=' pending'), 
    path('proprety/image/delete/<int:img_id>',ImagesListAPIView.as_view(), name='image-delete '),
    path('proprety/search/',SearchKeywordAPIVIEW.as_view(),name='Search'), #post
    path('proprety/filter/',SearchFilterAPIVIEW.as_view(),name='Filter'), #post


]