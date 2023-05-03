from django.urls import path
from django.urls import re_path as url 
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from automotive.views import (BrandsHomeAPIView,BrandListAPIView ,BrandModelListview,CategoryListAPIView,SubcategoryListview
                                ,AutomotiveListAPIView,FavoritApiView,MyAutomotiveAPIView,SearchKeywordAPIVIEW,
                                BarndAutomotiveAPIView,HomeAutomotiveAPIView,SearchFilterAPIVIEW,
                                MyAutomotiveActiveApiView,MyAutomotiveDisActiveApiView,MyAutomotivePendingApiView,
                                MyAutomotiveRejectApiView,ImagesListAPIView,CategoryWebListAPIView,ayman)
router = DefaultRouter()
urlpatterns = [
    path('', include(router.urls)), 
    path('brands/home',BrandsHomeAPIView.as_view(), name='brand-home'),
    path('brands/',BrandListAPIView.as_view(), name='brand-list'),
    path('cats/',CategoryListAPIView.as_view(), name='cats-list'),
    path('webcats/',CategoryWebListAPIView.as_view(), name='cats-list'),

    url(r'^cats/(?P<id>[0-9]+)/brands/$', BrandListAPIView.as_view(), name='Brands'),

    url(r'^brands/(?P<id>[0-9]+)/model/$', BrandModelListview.as_view(), name='Models'),
    url(r'^cats/(?P<id>[0-9]+)/subcats/$', SubcategoryListview.as_view(), name='sub category'),
    path('automotive/add/',AutomotiveListAPIView.as_view(), name='autiomotive-post '), #post
    path('automotive/view/<int:auto_id>', AutomotiveListAPIView.as_view(), name='autiomotive-view'),
        #get
    path('automotive/update/<int:auto_id>',AutomotiveListAPIView.as_view(), name='autiomotive-update '),
        #put 
    path('automotive/delete/<int:auto_id>',AutomotiveListAPIView.as_view(), name='autiomotive-delete '),
        #delete 
    path('automotive/active/<int:auto_id>', AutomotiveListAPIView.as_view(), name='autiomotive-Active_Upadte'),
        #patch
    path('automotive/fav/',FavoritApiView.as_view(),name='favorit'), #post
    path('automotive/myfav/',FavoritApiView.as_view(),name='my favorit'), # get
    path('automotive/myauto/',MyAutomotiveAPIView.as_view(),name='my autoMotive'), # get
    path('automotive/brands/<int:brand_id>',BarndAutomotiveAPIView.as_view(),name='my autoMotive'), # get

    path('automotive/search/',SearchKeywordAPIVIEW.as_view(),name='Search'), #post
    path('automotive/filter/',SearchFilterAPIVIEW.as_view(),name='Filter'), #post

    
    path('automotive/home/<str:type_auto>',HomeAutomotiveAPIView.as_view(),name='All - New - Used Home'), #get

    path('automotive/myautomotive/active/',MyAutomotiveActiveApiView.as_view(),name='Active'), 
    path('automotive/myautomotive/disactive/',MyAutomotiveDisActiveApiView.as_view(),name=' Dis active'), 
    path('automotive/myautomotive/reject/',MyAutomotiveRejectApiView.as_view(),name=' reject'), 
    path('automotive/myautomotive/pending/',MyAutomotivePendingApiView.as_view(),name=' pending'), 
    path('aym/',ayman.as_view(),name='All - New - Used Home'), #post
    path('automotive/image/delete/<int:img_id>',ImagesListAPIView.as_view(), name='image-delete '),

 

]