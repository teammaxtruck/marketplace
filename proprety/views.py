from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.pagination import  PageNumberPagination
from django.shortcuts import get_object_or_404

from rest_framework import status,generics
from proprety.serializers import (CategoryNameSerializer,CategoryWebNameSerializer, SubcatListSerializer,propretySerializer,propretyDetalsSerializer,
                                  propretyFavSerializer,FavoritSerializer)
from proprety.models import (Category,SubCategory,proprety,propretyimages,propretyfave)

# Create your views here.

class CategoryListAPIView(generics.ListAPIView):

   def get(self, request, format=None):
    queryset =Category.objects.all()
    serializer = CategoryNameSerializer(queryset, many=True)
    counts=len(serializer.data)
    expected_data = {
              "count":counts,
              "Categories":serializer.data ,}
    json_data = {
        "code" : 200,
        "message" : "success",
        "data" :expected_data
        }
    return Response(json_data, status=status.HTTP_200_OK)
   
class CategoryWebListAPIView(generics.ListAPIView):

   def get(self, request, format=None):
    queryset =Category.objects.all()
    serializer = CategoryWebNameSerializer(queryset, many=True)
    counts=len(serializer.data)
    expected_data = {
              "count":counts,
              "Categories":serializer.data ,}
    json_data = {
        "code" : 200,
        "message" : "success",
        "data" :expected_data
        }
    return Response(json_data, status=status.HTTP_200_OK)
   
class SubcategoryListview(generics.ListAPIView):
    serializer_class = SubcatListSerializer
    queryset = SubCategory.objects.all()
    def list(self, request, *args, **kwargs):
        category_id = self.kwargs['id']
        category= get_object_or_404(Category, id=category_id)
        subcategory = SubCategory.objects.filter(category_id=category.id)
        ser = SubcatListSerializer(subcategory, many=True).data
        counts=len(ser)
        expected_data = {
              "count":counts,
              "Subcategores":ser ,}
        json_data = {
        "code" : 200,
        "message" : "success",
        "data" :expected_data
        }
        return Response(json_data, status=status.HTTP_200_OK)
    
class PropretyListAPIView(APIView):
   permission_classes = [IsAuthenticated]
   def post(self, request, format=None):
    request.data._mutable = True
    request.data['uid'] = request.user.id

    uid=request.user.id
  

    files = request.FILES.getlist('image')
    if files:
      request.data.pop('image')
      serializer = propretySerializer(data=request.data)
      request.data._mutable = False

      if serializer.is_valid():
          serializer.save(uid_id=uid)
          last_id = proprety.objects.get(id=serializer.data['id'])

          uploaded_files = []
          a=0
          for file in files:
            is_main=False
            a=a+1
            if a ==1 :
              is_main= True
            content = propretyimages.objects.create(proprety=last_id, proprety_image=file,is_main=is_main)
            uploaded_files.append(content)


          json_data = {
                  "code" : 200,
                  "Uid": request.user.id,
                  "message" : "success",
                  "proprety":serializer.data

                  }

          return Response(json_data, status=status.HTTP_200_OK)

      Error_data = {
                  "code" : 400,

                  "message" : "Error",
                  "error" :serializer.errors


                  }
      return Response(Error_data, status=status.HTTP_400_BAD_REQUEST)

   def get_object(self, prop_id):
        '''
        Helper method to get the object with given prop_id
        '''
        try:
            return proprety.objects.get(id=prop_id )
        except proprety.DoesNotExist:
            return None
   def get_images(self, prop_id):
        '''
        Helper method to get the object with given prop_id
        '''
        try:
            return  propretyimages.objects.get(proprety=prop_id )
        except propretyimages.DoesNotExist:
            return None
    # 3. Retrieve
   def get(self, request, prop_id, *args, **kwargs):

        '''
        Retrieves the proprety with given prop_id
        '''

        auto_instance = self.get_object(prop_id)
        if not auto_instance:
            return Response(
                {"res": "Object with items id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        propretys=proprety.objects.filter(id=prop_id)

        view =propretys[0].view +1
        propretys=proprety.objects.filter(id=prop_id).update(view=view)
        serializer = propretyDetalsSerializer(auto_instance)


        json_data = {
      "code" : 200,
      "message" : "success",
      "proprety":serializer.data,
       }

        return Response(json_data, status=status.HTTP_200_OK)

   def delete(self, request, prop_id, *args, **kwargs):
        '''
        Deletes the proprety item with given id if exists
        '''
        auto_instance = self.get_object(prop_id)
        if not auto_instance:
            return Response(
                {"res": "Object with proprety id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        img_instance=propretyimages.objects.filter(proprety=prop_id).delete()
       # ads=countrypropretyads.objects.filter(proprety=prop_id).delete()

        auto_instance.delete()

        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
   def patch(self, request, prop_id, *args, **kwargs):
        prod_instance = self.get_object(prop_id)
        activeproprety=proprety.objects.filter(id=prop_id)
        if activeproprety[0].is_active==0 :
           is_active=1
        else : is_active=0
        serializer = propretySerializer(instance = prod_instance, data = {'is_active':is_active}, partial = True)
        if serializer.is_valid():
            serializer.save()
            json_data={
            "code" : 200,
            "message" : "success",
            "proprety":serializer.data
            }
            return Response(json_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   def put(self, request, prop_id, *args, **kwargs):
        '''
         '''
        auto_instance = self.get_object(prop_id)
        if not auto_instance:
            return Response(
                {"res": "Object with proudcts id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'title': request.data.get('title'),
            'prop_type': request.data.get('prop_type'),
            'category': request.data.get('category'),
            'subcategory': request.data.get('subcategory'),
            'price': request.data.get('price'),
            'currency': request.data.get('currency'),
            'country': request.data.get('country'),
            'state': request.data.get('state'),
            'city': request.data.get('city'),
            'address':request.data.get('address'),
            'area': request.data.get('area'),
            'areaunit': request.data.get('areaunit'),
            'bedrooms':request.data.get('bedrooms'),
            'baths':request.data.get('baths'),
            'furnished':request.data.get('furnished'),
            'living_room':request.data.get('living_room'),
            'balcony':request.data.get('balcony'),
            'lift':request.data.get('lift'),
            'parking':request.data.get('parking'),
            'storage':request.data.get('storage'),
            'gym':request.data.get('gym'),
            'cinema':request.data.get('cinema'),   
            'conference':request.data.get('conference'),
            'swimming_poll':request.data.get('swimming_poll'),
            'maid_room':request.data.get('maid_room'),
            'sports':request.data.get('sports'),
            'linkurl':request.data.get('linkurl'),
            'description':request.data.get('description'),
            'is_publish':False,
        }
        serializer = propretySerializer(instance = auto_instance, data=data, partial = True)
        if serializer.is_valid():
          serializer.save()
          files = request.FILES.getlist('image')
          if files:
                request.data.pop('image')
                uploaded_files = []
                a=0
                for file in files:
                    is_main=False
                    a=a+1
                    if a ==1 :
                      is_main= True

                    content = propretyimages.objects.create(proprety_id=prop_id, proprety_image=file,is_main=is_main)
                    uploaded_files.append(content)

          
          json_data = {
                    "code" : 200,
                    "Uid": request.user.id,
                    "message" : "success",
                    "proprety":serializer.data

                    }

          return Response(json_data, status=status.HTTP_200_OK)

        Error_data = {
                  "code" : 400,
                  "message" : "Error",
                  "error" :serializer.errors


                  }
        return Response(Error_data, status=status.HTTP_400_BAD_REQUEST)
       



class MyPropretyAPIView(APIView):
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):

    uid=request.user.id
    sql='SELECT f.is_fav,p.id from proprety_proprety p left JOIN  proprety_propretyfave f on p.id = f.proprety_id AND f.uid_id=%(uid)s'
    #sql='SELECT f.is_fav,a.id from automotive_automotive a left JOIN  automotive_automotivefave f on a.id = f.automotive_id  AND f.uid_id=%s '
    sql=sql+' ORDER BY p.id desc  '
    #
    #sql=sql+'  WHERE ( p.is_active=1 And p.is_publish=1 )  ORDER BY a.id desc limit 10 '


    queryset = proprety.objects.raw(sql,[uid])
    serializer=propretyFavSerializer(queryset,many=True).data
    counts=len(serializer)
    expected_data = {
           "count":counts,
          "Proprety":serializer }
    json_data = {
      "code" : 200,
      "message" : "success",
      "data" :expected_data
      }
    return Response(json_data, status=status.HTTP_200_OK)


class HomeApropretyAPIView(APIView):
  permission_classes = [IsAuthenticated]
  #def get(self, request, auto_id, *args, **kwargs):
  def get(self, request, prop_type, *args, **kwargs):


    uid=request.user
  
    sql='SELECT f.is_fav,p.id from proprety_proprety p left JOIN  proprety_propretyfave f on p.id = f.proprety_id AND f.uid_id=%(uid)s'
   # sql=sql +'  WHERE ' ##( p.is_active=1 And p.is_publish=1) '

    if prop_type=="Rent" or prop_type=="Sael" :
       sql=sql+ 'WHERE  p.prop_type LIKE %(prop_type)s   '
    sql=sql+'  ORDER BY p.id desc'
    #


    params={"uid":uid,"prop_type":'%'+prop_type+'%', }
    queryset = proprety.objects.raw(sql,params)

    serializer=propretyFavSerializer(queryset,many=True).data
    count_all=len(serializer)
    page_query_param = 'page'
    page_size = 10
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    paginator.page_query_param = page_query_param

    zero=len(serializer)%10
    count_page=round(len(serializer)/10)
    if zero!=0 and count_all>10: count_page=count_page+1
    p = paginator.paginate_queryset(queryset, request=request) # change 1
    serializer=propretyFavSerializer(p,many=True).data
    counts=len(serializer)
    expected_data = {
           "count":counts,
            "count_all":count_all,
            "count_page":count_page,
          "proprety":serializer }
    json_data = {
      "code" : 200,
      "message" : "success",
      "data" :expected_data
      }
    return Response(json_data, status=status.HTTP_200_OK)
class CatpropretyAPIView(APIView):
  permission_classes = [IsAuthenticated]
  def get(self, request, cat_id, *args, **kwargs):
    uid=request.user
    sql='SELECT f.is_fav,p.id from proprety_proprety p left JOIN  proprety_propretyfave f on p.id = f.proprety_id AND f.uid_id=%(uid)s'
   # sql=sql +'  WHERE ' ##( p.is_active=1 And p.is_publish=1) '
    sql=sql+ 'WHERE  p.category_id LIKE %(cat_id)s   '
    sql=sql+'  ORDER BY p.id desc'
    #


    params={"uid":uid,"cat_id":cat_id, }
    queryset = proprety.objects.raw(sql,params)

    serializer=propretyFavSerializer(queryset,many=True).data
    count_all=len(serializer)
    page_query_param = 'page'
    page_size = 10
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    paginator.page_query_param = page_query_param

    zero=len(serializer)%10
    count_page=round(len(serializer)/10)
    if zero!=0 and count_all>10: count_page=count_page+1
    p = paginator.paginate_queryset(queryset, request=request) # change 1
    serializer=propretyFavSerializer(p,many=True).data
    counts=len(serializer)
    expected_data = {
           "count":counts,
            "count_all":count_all,
            "count_page":count_page,
          "proprety":serializer }
    json_data = {
      "code" : 200,
      "message" : "success",
      "data" :expected_data
      }
    return Response(json_data, status=status.HTTP_200_OK)

class PropFavoritApiView(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
        uid=request.user.id
        request.data._mutable = True
        request.data['uid'] = uid
        request.data['is_fav']=True
        proprety=request.data['proprety']
        request.data._mutable = False
        fav=propretyfave.objects.filter(uid_id=uid,proprety_id=proprety)
        count=len(fav)
        if count==1:
          fav.delete()
          fav_ser="Delete"
        else :
          serializer=FavoritSerializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save()
          fav_ser=serializer.data

        json_data = {

          "code" : 200,
           "message" : "success",
          "fav":fav_ser
          }
        return Response(json_data, status=status.HTTP_200_OK)

  def get(self,request,format=None):

    uid=request.user.id
    sql='SELECT * FROM proprety_proprety WHERE id IN( SELECT proprety_id FROM proprety_propretyfave where uid_id=%s)'

    queryset = Proprety.objects.raw(sql,[uid])
    serializer = propretyFavSerializer(queryset, many=True)
    counts=len(serializer.data)
    expected_data = {
           "count":counts,
           "My Proprety Favorite":serializer.data ,
            }
    json_data = {
      "code" : 200,
      "message" : "success",
      "data" :expected_data
      }
    return Response(json_data, status=status.HTTP_200_OK)

class MyPropretyActiveApiView(APIView):
  permission_classes = [IsAuthenticated]
  def get(self,request,format=None):
    uid=request.user
    proprety= proprety.objects.filter(uid=uid.id,is_active=1,is_publish=1).order_by('-id')
    serializer = propretyFavSerializer(proprety, many=True)
    counts=len(serializer.data)
    expected_data = {
           "count":counts,
            "My proprety Active":serializer.data ,}
    json_data = {
      "code" : 200,
      "message" : "success",
      "data" :expected_data
      }
    return Response(json_data, status=status.HTTP_200_OK)
class  MyPropretyDisActiveApiView(APIView):
  permission_classes = [IsAuthenticated]
  def get(self,request,format=None):
    uid=request.user
    proprety= proprety.objects.filter(uid=uid.id,is_active=0,is_publish=1).order_by('-id')
    serializer = propretyFavSerializer(proprety, many=True)
    counts=len(serializer.data)
    expected_data = {
           "count":counts,
            "My proprety Dis Active":serializer.data ,}
    json_data = {
      "code" : 200,
      "message" : "success",
      "data" :expected_data
      }
    return Response(json_data, status=status.HTTP_200_OK)


class  MyPropretyPendingApiView(APIView):
   permission_classes = [IsAuthenticated]
   def get(self,request,format=None):
    uid=request.user
    propretys= proprety.objects.filter(uid=uid.id,is_publish=0,is_active=1).order_by('-id')
    serializer = propretyFavSerializer(propretys, many=True)
    counts=len(serializer.data)
    expected_data = {
           "count":counts,
            "My proprety pending":serializer.data ,}
    json_data = {
      "code" : 200,
      "message" : "success",
      "data" :expected_data
      }
    return Response(json_data, status=status.HTTP_200_OK)

class MyPropretyRejectApiView(APIView):
  permission_classes = [IsAuthenticated]
  def get(self,request,format=None):
    uid=request.user
    propretys= proprety.objects.filter(uid=uid.id,is_reject=1).order_by('-id')
    serializer = propretyFavSerializer(propretys, many=True)
    counts=len(serializer.data)
    expected_data = {
           "count":counts,
            "My proprety Reject":serializer.data ,}
    json_data = {
      "code" : 200,
      "message" : "success",
      "data" :expected_data
      }
    return Response(json_data, status=status.HTTP_200_OK)
class ImagesListAPIView(APIView):
     permission_classes = [IsAuthenticated]
     def get_object(self, img_id):
        '''
        Helper method to get the object with given pro_id
        '''
        try:
            return propretyimages.objects.get(id=img_id )
        except propretyimages.DoesNotExist:
            return None

     def delete(self, request, img_id, *args, **kwargs):
        '''
        Deletes the images item with given id if exists
        '''


        img_instance = self.get_object(img_id)
       # img_instance =Images.objects.get(id=img_id )
        if not img_instance:
            return Response(
                {"res": "Object with products id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        img_instance.delete()


        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class SearchKeywordAPIVIEW(APIView):
  permission_classes = [IsAuthenticated]
  #def get(self,request):
  def post(self, request, format=None):
      uid=request.user.id
      pattern=request.data.get('search')

     #####
     
      cats=Category.objects.filter(name__icontains=pattern)
      cats_id=[]
      for k in range(len(cats)):
        cats_id.append(cats[k].id)
      #####
      subcats=SubCategory.objects.filter(name__icontains=pattern)
      subcats_id=[]
      for m in range(len(subcats)):
        subcats_id.append(subcats[m].id)

      sql='SELECT f.is_fav,p.id from proprety_proprety p left JOIN  proprety_propretyfave f on p.id = f.proprety_id '
      sql=sql+'AND f.uid_id=%(uid)s WHERE ( p.is_active=1 And p.is_publish=1 ) AND '
      sql=sql+'(p.title LIKE %(title)s  OR  p.description LIKE %(description)s OR '
      sql=sql+'p.prop_type LIKE %(prop_type)s  OR  '
      sql=sql+'p.address LIKE %(address)s  OR  p.bedrooms LIKE %(bedrooms)s  OR '
      sql=sql+'p.areaunit LIKE %(areaunit)s  OR  p.baths LIKE %(baths)s ) '
     
      if len(cats) !=0 :
        sql=sql+ 'OR  p.category_id IN %(category_id)s  '
      if len(subcats)!=0 :
         sql=sql+ 'OR p.subcategory_id IN %(subcat)s '

      sql=sql+' ORDER BY p.id desc '

      params={"uid":uid,"title":'%'+pattern+'%',"description":'%'+pattern+'%','category_id':cats_id,"subcat":subcats_id,
                "prop_type":'%'+pattern+'%',"address":'%'+pattern+'%',"bedrooms":'%'+pattern+'%',"areaunit":'%'+pattern+'%',"baths":'%'+pattern+'%'
                }
      queryset = proprety.objects.raw(sql,params)
      serializer=propretyFavSerializer(queryset,many=True).data
      counts=len(serializer)
      expected_data = {
            "count":counts,
            "result":serializer ,}

      json_data = {
        "code" : 200,
        "message" : "success",
        "data" :expected_data
      }
      return Response(json_data, status=status.HTTP_200_OK)
class SearchFilterAPIVIEW(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
         uid=request.user.id
         prop_type= request.data.get('prop_type')
         category= request.data.get('category')
         subcat= request.data.get('subcat')
         price= request.data.get('price')
         currency= request.data.get('currency')
         country= request.data.get('country')
         state= request.data.get('state')
         city= request.data.get('city')
         areaunit= request.data.get('areaunit')
         bedrooms=request.data.get('bedrooms')
         baths=request.data.get('baths')
         furnished=request.data.get('furnished')
         living_room=request.data.get('living_room')
         balcony=request.data.get('balcony')
         lift=request.data.get('lift')
         parking=request.data.get('parking')
         storage=request.data.get('storage')
         gym=request.data.get('gym')
         cinema=request.data.get('cinema')   
         conference=request.data.get('conference')
         swimming_poll=request.data.get('swimming_poll')
         maid_room=request.data.get('maid_room')
         sports=request.data.get('sports')       
         minprice=request.data.get('minprice') 
         maxprice=request.data.get('maxprice') 

         sql='SELECT f.is_fav,p.id from proprety_proprety p left JOIN  proprety_propretyfave f on p.id = f.proprety_id '
         sql=sql+'AND f.uid_id=%(uid)s WHERE ( p.is_active=1 And p.is_publish=1 ) '

         if prop_type !="" :
            sql=sql+'And ( p.prop_type LIKE %(prop_type)s)'
         if areaunit =="Select Area Unit": areaunit=""
         if areaunit !="" :
            sql=sql+'And ( p.areaunit LIKE %(areaunit)s)'
        
         if bedrooms !="" :
            sql=sql+'And ( p.bedrooms LIKE %(bedrooms)s)'
       
         if baths !="":
            sql=sql+'And ( p.baths LIKE %(baths)s)'
        
         if balcony !="" :
            sql=sql+'And ( p.balcony = %(balcony)s)'
         if lift !="" :
            sql=sql+'And ( p.lift = %(lift)s)'
         if storage !="" :
            sql=sql+'And ( p.storage = %(storage)s)'
         if maid_room !="" :
            sql=sql+'And ( p.maid_room = %(maid_room)s)'
         if swimming_poll !="" :
            sql=sql+'And ( p.swimming_poll = %(swimming_poll)s)'
         if cinema !="" :
            sql=sql+'And ( p.cinema = %(cinema)s)'
         if parking !="" :
            sql=sql+'And ( p.parking = %(parking)s)'
    
         if conference !="" :
            sql=sql+'And ( p.conference = %(conference)s)'
         if sports !="" :
            sql=sql+'And ( p.sports = %(sports)s)'
   
         if furnished !="" :
            sql=sql+'And ( p.furnished = %(furnished)s)'
         if living_room !="" :
            sql=sql+'And ( p.living_room = %(living_room)s)'
        
         if maxprice !="" and minprice !="" :
          sql=sql+ 'And (p.price BETWEEN %(minprice)s AND %(maxprice)s)'
         if category !="":
            sql=sql+'And (p.category_id = %(category_id)s)'
         if  subcat !="" :
              sql=sql+'And (p.subcategory_id =%(subcat)s)'
         if country !="":
            sql=sql+'And (p.country_id =%(country_id)s)'
         if state !="":
            sql=sql+'And (p.state_id =%(state_id)s)'
         if city !="":
            sql=sql+'And (p.city_id =%(city_id)s)'

         if currency!="":
            sql=sql+'And (p.currency LIKE %(currency)s)'

         sql=sql+" ORDER BY p.id desc "

         params={"uid":uid,'category_id':category,'areaunit' :areaunit,"prop_type":'%'+prop_type+'%',"subcat":subcat,
                    "bedrooms":'%'+bedrooms+'%',"baths":'%'+baths+'%',"currency":'%'+currency+'%',
                    "furnished":furnished,"living_room":living_room,"balcony":balcony,"lift":lift,
                    "parking":parking,"storage":storage,"gym":gym,"cinema":cinema,
                    "conference":conference,"swimming_poll":swimming_poll,"maid_room":maid_room,"sports":sports,
                    "sports":sports,"country_id":country,"state_id":state,"city_id":city,
                    "maxprice":maxprice,"minprice":minprice,
              
                    }

         queryset = proprety.objects.raw(sql,params)
         serializer=propretyFavSerializer(queryset,many=True).data
         counts=len(serializer)

         expected_data = {
                "count":counts,
                "result":serializer ,}

         json_data = {
            "code" : 200,
            "message" : "success",
            "data" :expected_data
          }
         return Response(json_data, status=status.HTTP_200_OK)
