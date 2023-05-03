from django.urls import path
from django.urls import re_path as url 
from django.conf.urls import include
 
from rest_framework.routers import DefaultRouter
from usersapp.views import  UserLoginView,UserRegistrationView,UserProfileView,UserUpadteImage,SendPasswordResetEmailView,UserChangePasswordView
from usersapp.views import  CountryListView,StateListView,CityListView,KeyListView,LanguageListView,UserWebRegistrationView,UserWebLoginView,UserwebProfileView

router = DefaultRouter()
urlpatterns = [
 
    path('', include(router.urls)), 
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('webregister/', UserWebRegistrationView.as_view(), name='register'),
    path('weblogin/', UserWebLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('webprofile/', UserwebProfileView.as_view(), name='webprofile'),
    path('profile/update/', UserProfileView.as_view(), name='Edit Profile image'),
    path('profile/update/img/', UserUpadteImage.as_view(), name='Edit Profile image'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    url(r'^countries/$', CountryListView.as_view(), name='countries'),
    # """List States            : api/states/id:country id""",
    # """Method: GET """,       """,
    url(r'^countries/(?P<id>[0-9]+)/states/$', StateListView.as_view(), name='state'),
    # """List Cities            : api/cities/id:state id""",
    # """Method: GET """,       """,
    url(r'^states/(?P<id>[0-9]+)/cities/$', CityListView.as_view(), name='city'),
    path('lang/<str:lang>',KeyListView.as_view(),name='Lang ar - en'), #get
    path('langs/',LanguageListView.as_view(),name='Langs ar - en'), #get




]