from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter
from rest_framework import generics,status
from rest_framework.response import Response

#from usersapp. 
from usersapp.renderers import UserRenderer
from usersapp.serializers import UserwebProfileSerializer,UserRegistrationSerializer,UserLoginSerializer,UserPutProfileSerializer,UserProfileSerializer,SendPasswordResetEmailSerializer,UserChangePasswordSerializer
from usersapp.serializers import CountrySerializer,StateSerializer,CitySerializer,KeylangSerializer,LanguageSerializer
from usersapp.models import User,Country,State,City,Language,Keylang

def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
     # 'refresh': str(refresh),,
      'token': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  # renderer_classes = [UserRenderer]

  def post(self, request, format=None):
   # type_user=request.data['type_user']
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    image='images/users/person.png'
    expected_data = {
 
            "token":token,
            "uid":user.id,
            "fullname":user.fullname,
            "email":user.email,
            "profile_image":image
            }
    json_data = {
      "code" : 200,
      "message" : "success",
      "data" :expected_data
      }
    return Response(json_data, status=status.HTTP_200_OK)


class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
   
    #request.data['email']=request.data['email'].lower()
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
        #token,created=Token.objects.get_or_create(user=user)
        token = get_tokens_for_user(user)
        image='images/users/person.png'
      
        expected_data = {
                      "token":token,
                      "uid":user.id,
                      "fullname":user.fullname,
                      "image" :"media/"+image}

        json_data = {
                "code" : 200,
                "message" : "success",
                "data" :expected_data
                }
        return Response(json_data, status=status.HTTP_200_OK)

              # return Response({'code':200,'msg':'success','data':token},status=status.HTTP_200_OK)
    else:
          Error_data = {
                "code" : 400,
                "message" : "Faild",
                "Error" :'Email or Password is not Valid'
                }
          return Response(Error_data, status=status.HTTP_404_NOT_FOUND)

class UserWebRegistrationView(APIView):
  # renderer_classes = [UserRenderer]

  def post(self, request, format=None):
   # type_user=request.data['type_user']
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    image='images/users/person.png'
    expected_data = {
 
            "token":token,
            "uid":user.id,
            "name":user.fullname,
            "email":user.email,
            "profile_image":image
            }
    json_data = {
      "code" : 200,
      "message" : "success",
      "data" :expected_data
      }
    return Response(json_data, status=status.HTTP_200_OK)

class UserWebLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
   
    #request.data['email']=request.data['email'].lower()
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
        #token,created=Token.objects.get_or_create(user=user)
        token = get_tokens_for_user(user)
        image='images/users/person.png'
        bg_image='images/users/grid.png'
        expected_data = {
            "token":token,
            "uid":user.id,
            "name":user.fullname,
            "email":user.email,
            "profile_image":image,
            "bg_image":bg_image,
            }

        json_data = {
                "code" : 200,
                "message" : "success",
                "data" :expected_data
                }
        return Response(json_data, status=status.HTTP_200_OK)

              # return Response({'code':200,'msg':'success','data':token},status=status.HTTP_200_OK)
    else:
          Error_data = {
                "code" : 400,
                "message" : "Faild",
                "Error" :'Email or Password is not Valid'
                }
          return Response(Error_data, status=status.HTTP_404_NOT_FOUND)

class UserwebProfileView (APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserwebProfileSerializer(request.user)
    
    json_data = {
            "code" : 200,
            "message" : "success",
            "data" :serializer.data,
           
            }
    return Response(json_data, status=status.HTTP_200_OK)
class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    country=request.user.country_id
    state=request.user.state_id
    city=request.user.city_id
    location={
       "countryId":country,
        "stateId":state,
         "cityId":city,    }
    json_data = {
            "code" : 200,
            "message" : "success",
            "data" :serializer.data,
            "location":location,
            }
    return Response(json_data, status=status.HTTP_200_OK)
  def put(self, request, *args, **kwargs):
        '''
         '''
        uid =request.user
      
        if not uid:
            return Response(
                {"res": "Object with Users id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not request.data.get('profile_image'):
             data = {
            'fullname': request.data.get('fullname'),
            'phone': request.data.get('phone'),
            'code':request.data.get('code'),
          #  'profile_image':  request.data.get('profile_image'),
            'country': request.data.get('country'),
            'state': request.data.get('state'),
            'city': request.data.get('city'),

                   }
        else :    
             data = {
            'fullname': request.data.get('fullname'),
            'phone': request.data.get('phone'),
            'code':request.data.get('code'),
            'profile_image':  request.data.get('profile_image'),
            'country': request.data.get('country'),
            'state': request.data.get('state'),
            'city': request.data.get('city'),
                    }
        serializer = UserPutProfileSerializer(instance = uid, data=data, partial = True)
        if serializer.is_valid():
           serializer.save()
           json_data = {
            "code" : 200,
            "message" : "success",
            "data" :serializer.data
           }
           return Response(json_data, status=status.HTTP_200_OK)
        Error_data = {
                "code" : 400,
                "message" : "Faild",
                "Error" :serializer.errors
                }
        return Response(Error_data, status=status.HTTP_404_NOT_FOUND)
       # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserUpadteImage(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, *args, **kwargs):
        '''
         '''
        uid =request.user
        data = {
              'profile_image':  request.data.get('profile_image'),
            'bg_image':request.data.get('bg_image')
            }
        if request.data.get('profile_image') and not request.data.get('bg_image'):
          data = {
            'profile_image':  request.data.get('profile_image'),
           }
        if not request.data.get('profile_image') and  request.data.get('bg_image'):
          data = {
            'bg_image':  request.data.get('bg_image'),
             }
        
        serializer = UserPutProfileSerializer(instance = uid, data=data, partial = True)
        if serializer.is_valid():
           serializer.save()
           json_data = {
            "code" : 200,
            "message" : "success",
            "data" :serializer.data
             }
           return Response(json_data, status=status.HTTP_200_OK)
        Error_data = {
                "code" : 400,
                "message" : "Faild",
                "Error" :serializer.errors
                }
        return Response(Error_data, status=status.HTTP_404_NOT_FOUND)

       
class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    if serializer.is_valid():
      serializer.is_valid(raise_exception=True)
      json_data = {
          "code" : 200,
          "message" : "success",
          "data" :'msg :Password Changed Successfully'
          }
      return Response(json_data, status=status.HTTP_200_OK)
    Error_data = {
                "code" : 400,
                "message" : "Faild",
                "Error" :serializer.errors
                }
    return Response(Error_data, status=status.HTTP_404_NOT_FOUND)
import random
class SendPasswordResetEmailView(APIView):

  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
   
   # my_list = [1, 2, 3, 4, 5, 6,7,8,9,0]
    rand_num = random.randrange(1000,9999)
    print(rand_num)
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email',"rand_num":rand_num}, status=status.HTTP_200_OK)

#--------------------country state city ------------------------
class CountryListView(generics.ListAPIView):

   def get(self, request, format=None):
    queryset =Country.objects.all()
    serializer = CountrySerializer(queryset, many=True)
    theData= serializer.data
    counts=len(serializer.data)
    expected_data = {
            # "count_page":count_page,
              "count":counts,
              "Countries":serializer.data ,}
    json_data = {
        "code" : 200,
        "message" : "success",
        "data" :expected_data
        }
    return Response(json_data, status=status.HTTP_200_OK)


class StateListView(generics.ListAPIView):
    serializer_class = StateSerializer
    queryset = State.objects.all()
    def list(self, request, *args, **kwargs):
        country_id = self.kwargs['id']
        country = get_object_or_404(Country, id=country_id)
        state = State.objects.filter(country_id=country.id)
        ser = StateSerializer(state, many=True).data
        counts=len(ser)
        expected_data = {
              "count":counts,
              "States":ser ,}
        json_data = {
        "code" : 200,
        "message" : "success",
        "data" :expected_data
        }
        return Response(json_data, status=status.HTTP_200_OK)
        #return Response(ser, status=status.HTTP_200_OK)


class CityListView(generics.ListAPIView):
    serializer_class = CitySerializer
    queryset = State.objects.all()

    def list(self, request, *args, **kwargs):
        state_id = self.kwargs['id']
        state = get_object_or_404(State, id=state_id)
        city = City.objects.filter(state_id=state.id)
        ser = CitySerializer(city, many=True).data
        counts=len(ser)
        expected_data = {
              "count":counts,
              "Cities":ser ,}
        json_data = {
        "code" : 200,
        "message" : "success",
        "data" :expected_data
        }
        return Response(json_data, status=status.HTTP_200_OK)

class KeyListView(generics.ListAPIView):
    def get(self, request, lang, *args, **kwargs):

        sql='SELECT * FROM usersapp_keylang,usersapp_language WHERE usersapp_language.id=usersapp_keylang.lang_id AND usersapp_language.code =%s'
        queryset = Keylang.objects.raw(sql,[lang])
        ser = KeylangSerializer(queryset, many=True).data
        counts=len(ser)
        expected_data = {
              "count":counts,
              "Keys":ser ,}
        json_data = {
        "code" : 200,
        "message" : "success",
        "data" :expected_data
        }
        return Response(json_data, status=status.HTTP_200_OK)
class LanguageListView(generics.ListAPIView):
    def get(self, request,  *args, **kwargs):

        queryset = Language.objects.all()
        ser = LanguageSerializer(queryset, many=True).data
        counts=len(ser)
        expected_data = {
              "count":counts,
              "language":ser ,}
        json_data = {
        "code" : 200,
        "message" : "success",
        "data" :expected_data
        }
        return Response(json_data, status=status.HTTP_200_OK)
