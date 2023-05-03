from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.pagination import  PageNumberPagination
from django.shortcuts import get_object_or_404

from rest_framework import status,generics
from automotive.serializers import (BrandHomeSerializer, BrandNameSerializer,BrandModelListSerializer,CategoryNameSerializer,
                                    CategoryWebNameSerializer,SubcatListSerializer,AutomotiveSerializer,AutomotiveDetalsSerializer,FavoritSerializer,
                                    AutomotiveFavSerializer)
from automotive.models import (Brands,BrandModels ,Categories,Subcatgoriess,Automotive,automotiveimages,
                               automotivefave,countryautomotiveads)
# Create your views here.

class BrandsHomeAPIView(APIView):

    # if there is something in items else raise error
  def get(self, request, format=None):
     sql='SELECT * FROM automotive_brands where is_home=True'
     brands = Brands.objects.raw(sql)
     serializer = BrandHomeSerializer(brands, many=True).data
     counts=len(serializer)
     expected_data = {
            "count":counts,
            "AutomotiveBrands":serializer ,}
     json_data = {
      "code" : 200,
      "message" : "success",
       "data" :expected_data
       }
     return Response(json_data, status=status.HTTP_200_OK)

class BrandListAPIView(generics.ListAPIView):

  queryset = Categories.objects.all()
  def list(self, request, *args, **kwargs):

        cat_id = self.kwargs['id']
        catbrand = Brands.objects.filter(cat=cat_id)
        serializer = BrandNameSerializer(catbrand, many=True).data
        counts=len(serializer)
        expected_data = {
             "count":counts,
              "Brands":serializer ,}
        json_data = {
        "code" : 200,
        "message" : "success",
        "data" :expected_data
        }
        return Response(json_data, status=status.HTTP_200_OK)

'''
  def get(self, request, format=None):

    brands =Brands.objects.all()
    serializer = BrandNameSerializer(brands, many=True)

    counts=len(serializer.data)
    expected_data = {
             "count":counts,
              "Brands":serializer.data ,}
    json_data = {
        "code" : 200,
        "message" : "success",
        "data" :expected_data
        }
    return Response(json_data, status=status.HTTP_200_OK)
 '''
class BrandModelListview(generics.ListAPIView):
    serializer_class = BrandModelListSerializer
    queryset = BrandModels.objects.all()
    def list(self, request, *args, **kwargs):
        brand_id = self.kwargs['id']
        brand= get_object_or_404(Brands, id=brand_id)
        brandmodel = BrandModels.objects.filter(brand=brand.id)
        serializer = BrandModelListSerializer(brandmodel, many=True).data
        counts=len(serializer)
        expected_data = {
             "count":counts,
              "Models":serializer ,}
        json_data = {
        "code" : 200,
        "message" : "success",
        "data" :expected_data
        }
        return Response(json_data, status=status.HTTP_200_OK)

class CategoryListAPIView(generics.ListAPIView):

   def get(self, request, format=None):
    queryset =Categories.objects.all()
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
    queryset =Categories.objects.all()
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
    queryset = Subcatgoriess.objects.all()
    def list(self, request, *args, **kwargs):
        category_id = self.kwargs['id']
        category= get_object_or_404(Categories, id=category_id)
        subcategory = Subcatgoriess.objects.filter(cat_id=category.id)
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
####auto Motive

class AutomotiveListAPIView(APIView):
   permission_classes = [IsAuthenticated]
   def post(self, request, format=None):
    request.data._mutable = True
    request.data['uid'] = request.user.id
    list_country=request.data['list_country']
    list_state=request.data['list_state']
   # request.data['currency'] =233 #usa $
    uid=request.user.id
   #####
    countryads = list_country.split(",")
    for country in countryads:
         print(country)

    files = request.FILES.getlist('image')
    if files:
      request.data.pop('image')
      serializer = AutomotiveSerializer(data=request.data)
      request.data._mutable = False

      if serializer.is_valid():
          serializer.save(uid_id=uid)
          last_id = Automotive.objects.get(id=serializer.data['id'])
          mngads = countryautomotiveads.objects.create(automotive=last_id, listcountry=list_country,liststate=list_state,uid_id=uid)

          uploaded_files = []
          a=0
          for file in files:
            is_main=False
            a=a+1
            if a ==1 :
              is_main= True
            content = automotiveimages.objects.create(automotive=last_id, automotive_image=file,is_main=is_main)
            uploaded_files.append(content)


          json_data = {
                  "code" : 200,
                  "Uid": request.user.id,
                  "message" : "success",
                  "automotive":serializer.data

                  }

          return Response(json_data, status=status.HTTP_200_OK)

      Error_data = {
                  "code" : 400,
                  "message" : "Error",
                  "error" :serializer.errors }
      return Response(Error_data, status=status.HTTP_400_BAD_REQUEST)
   def get_object(self, auto_id):
        '''
        Helper method to get the object with given auto_id
        '''
        try:
            return Automotive.objects.get(id=auto_id )
        except Automotive.DoesNotExist:
            return None
   def get_images(self, auto_id):
        '''
        Helper method to get the object with given auto_id
        '''
        try:
            return automotiveimages.objects.get(automotive=auto_id )
        except automotiveimages.DoesNotExist:
            return None
    # 3. Retrieve
   def get(self, request, auto_id, *args, **kwargs):

        '''
        Retrieves the Automotive with given auto_id
        '''

        auto_instance = self.get_object(auto_id)
        if not auto_instance:
            return Response(
                {"res": "Object with items id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        automotives=Automotive.objects.filter(id=auto_id)

        view =automotives[0].view +1
        automotives=Automotive.objects.filter(id=auto_id).update(view=view)
        serializer = AutomotiveDetalsSerializer(auto_instance)


        json_data = {
      "code" : 200,
      "message" : "success",
      "Automotive":serializer.data,
       }

        return Response(json_data, status=status.HTTP_200_OK)

   def delete(self, request, auto_id, *args, **kwargs):
        '''
        Deletes the Automotive item with given id if exists
        '''
        auto_instance = self.get_object(auto_id)
        if not auto_instance:
            return Response(
                {"res": "Object with Automotive id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        img_instance=automotiveimages.objects.filter(automotive=auto_id).delete()
        ads=countryautomotiveads.objects.filter(automotive=auto_id).delete()

        auto_instance.delete()

        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
   def patch(self, request, auto_id, *args, **kwargs):
        prod_instance = self.get_object(auto_id)
        activeAutomotive=Automotive.objects.filter(id=auto_id)
        if activeAutomotive[0].is_active==0 :
           is_active=1
        else : is_active=0
        serializer = AutomotiveSerializer(instance = prod_instance, data = {'is_active':is_active}, partial = True)
        if serializer.is_valid():
            serializer.save()
            json_data={
            "code" : 200,
            "message" : "success",
            "Automotive":serializer.data
            }
            return Response(json_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   def put(self, request, auto_id, *args, **kwargs):
        '''
         '''
        auto_instance = self.get_object(auto_id)
        if not auto_instance:
            return Response(
                {"res": "Object with proudcts id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'title': request.data.get('title'),
            'auto_type': request.data.get('auto_type'),

            'brand': request.data.get('brand'),
            'cat': request.data.get('cat'),
            'subcat': request.data.get('subcat'),
            'brandmodel': request.data.get('brandmodel'),

            'price': request.data.get('price'),
            'currency': request.data.get('currency'),
            'country': request.data.get('country'),
            'state': request.data.get('state'),
            'city': request.data.get('city'),
            'address':request.data.get('address'),

            'year': request.data.get('year'),
            'kilometers': request.data.get('kilometers'),
            'color':request.data.get('color'),
            'fuel_type':request.data.get('fuel_type'),
            'body_condition':request.data.get('body_condition'),
            'inside_out':request.data.get('inside_out'),
            'transmission_type':request.data.get('transmission_type'),
            'door':request.data.get('door'),
            'power':request.data.get('power'),
            'specs':request.data.get('specs'),
            'cylinders':request.data.get('cylinders'),
            'streeingside':request.data.get('streeingside'),
            'linkurl':request.data.get('linkurl'),
            'description':request.data.get('description'),
            'is_publish':False,
        }
        serializer = AutomotiveSerializer(instance = auto_instance, data=data, partial = True)
        if serializer.is_valid():
              serializer.save()
        files = request.FILES.getlist('image')
        if files:
             # img_instance=automotiveimages.objects.filter(automotive=auto_id).delete()
              request.data.pop('image')
              uploaded_files = []
              a=0
              for file in files:
                  is_main=False
                  a=a+1
                  if a ==1 :
                    is_main= True

                  content = automotiveimages.objects.create(automotive_id=auto_id, automotive_image=file,is_main=is_main)
                  uploaded_files.append(content)

        return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavoritApiView(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
        uid=request.user.id
        request.data._mutable = True
        request.data['uid'] = uid
        request.data['is_fav']=True
        automotive=request.data['automotive']
        request.data._mutable = False
        fav=automotivefave.objects.filter(uid_id=uid,automotive_id=automotive)
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
    sql='SELECT * FROM automotive_automotive WHERE id IN( SELECT automotive_id FROM automotive_automotivefave where uid_id=%s)'

    queryset = Automotive.objects.raw(sql,[uid])
    serializer = AutomotiveDetalsSerializer(queryset, many=True)
    counts=len(serializer.data)
    expected_data = {
           "count":counts,
           "My Automotive Favorite":serializer.data ,
            }
    json_data = {
      "code" : 200,
      "message" : "success",
      "data" :expected_data
      }
    return Response(json_data, status=status.HTTP_200_OK)

class MyAutomotiveAPIView(APIView):
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):

    uid=request.user.id
    sql='SELECT f.is_fav,a.id from automotive_automotive a left JOIN  automotive_automotivefave f on a.id = f.automotive_id  AND f.uid_id=%s '
    sql=sql+' ORDER BY a.id desc  '
    #
    #sql=sql+'  WHERE ( a.is_active=1 And a.is_publish=1 )  ORDER BY a.id desc limit 10 '


    queryset = Automotive.objects.raw(sql,[uid])
    serializer=AutomotiveFavSerializer(queryset,many=True).data
    counts=len(serializer)
    expected_data = {
           "count":counts,
          "Automotive":serializer }
    json_data = {
      "code" : 200,
      "message" : "success",
      "data" :expected_data
      }
    return Response(json_data, status=status.HTTP_200_OK)


class HomeAutomotiveAPIView(APIView):
  permission_classes = [IsAuthenticated]
  #def get(self, request, auto_id, *args, **kwargs):
  def get(self, request, type_auto, *args, **kwargs):


    uid=request.user
    #####
    ####
    '''
    sql='SELECT f.is_fav,a.* from automotive_automotive a left JOIN  automotive_automotivefave f on a.id = f.automotive_id
    sql=sql+' WHERE a.id IN (SELECT automotive_id FROM automotive_countryautomotiveads WHERE listcountry LIKE %(listcountry)s '
    sql=sql+ 'and liststate LIKE %(liststate)s AND listcountry LIKE %(listcity)s)'
    queryset = Automotive.objects.raw(sql,[uid])
    params={"uid":uid,"listcountry":'%'+country+'%', "liststate":'%'+state+'%',"listcity":'%'+city+'%',
                }
    queryset = Automotive.objects.raw(sql,params)

    '''
    sql='SELECT f.is_fav,a.id from automotive_automotive a left JOIN  automotive_automotivefave f on a.id = f.automotive_id AND f.uid_id=%(uid)s '
   # sql=sql +'  WHERE ' ##( a.is_active=1 And a.is_publish=1) '

    if type_auto=="New" or type_auto=="Used" :
       sql=sql+ 'WHERE  a.auto_type LIKE %(auto_type)s   '
    sql=sql+'  ORDER BY a.id desc '
    #

    #sql=sql+'  WHERE ( a.is_active=1 And a.is_publish=1 )  ORDER BY a.id desc limit 10 '.

    params={"uid":uid,"auto_type":'%'+type_auto+'%', }
    queryset = Automotive.objects.raw(sql,params)

    serializer=AutomotiveFavSerializer(queryset,many=True).data
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
    serializer=AutomotiveFavSerializer(p,many=True).data
    counts=len(serializer)
    expected_data = {
           "count":counts,
            "count_all":count_all,
            "count_page":count_page,
          "automaotive":serializer }
    json_data = {
      "code" : 200,
      "message" : "success",
      "data" :expected_data
      }
    return Response(json_data, status=status.HTTP_200_OK)

class BarndAutomotiveAPIView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request, brand_id, *args, **kwargs):
    uid=request.user.id
    sql='SELECT f.is_fav,a.id from automotive_automotive a left JOIN  automotive_automotivefave f on a.id = f.automotive_id  AND f.uid_id=%(uid)s '
    sql=sql+' where a.brand_id = %(brand_id)s ORDER BY a.id desc  '
    #
    #sql=sql+'  WHERE ( a.is_active=1 And a.is_publish=1 )  ORDER BY a.id desc limit 10 '

    params={"uid":uid,'brand_id':brand_id}

    queryset = Automotive.objects.raw(sql,params)
    serializer=AutomotiveFavSerializer(queryset,many=True).data
    count_all=len(serializer)
    page_query_param = 'page'
    page_size = 10
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    paginator.page_query_param = page_query_param

    zero=len(serializer)%10
    count_page=round(len(serializer)/10)
    if zero!=0 and count_all<10: count_page=count_page+1
    p = paginator.paginate_queryset(queryset, request=request) # change 1
    serializer=AutomotiveFavSerializer(p,many=True).data
    counts=len(serializer)
    expected_data = {
           "count":counts,
            "count_all":count_all,
            "count_page":count_page,
          "automaotive":serializer }

    json_data = {
      "code" : 200,
      "message" : "success",
      "data" :expected_data
      }
    return Response(json_data, status=status.HTTP_200_OK)


class SearchKeywordAPIVIEW(APIView):
  permission_classes = [IsAuthenticated]
  #def get(self,request):
  def post(self, request, format=None):
      uid=request.user.id
      pattern=request.data.get('search')

     #####
      brands=Brands.objects.filter(name__icontains=pattern)
      brands_id=[]
      for i in range(len(brands)):
        brands_id.append(brands[i].id)
      #####
      brandmodels=BrandModels.objects.filter(name__icontains=pattern)
      brandmodels_id=[]
      for j in range(len(brandmodels)):
        brandmodels_id.append(brandmodels[j].id)
      #####
      cats=Categories.objects.filter(name__icontains=pattern)
      cats_id=[]
      for k in range(len(cats)):
        cats_id.append(cats[k].id)
      #####
      subcats=Subcatgoriess.objects.filter(name__icontains=pattern)
      subcats_id=[]
      for m in range(len(subcats)):
        subcats_id.append(subcats[m].id)

      sql='SELECT f.is_fav,a.id from automotive_automotive a left JOIN  automotive_automotivefave f on a.id = f.automotive_id '
      sql=sql+'AND f.uid_id=%(uid)s WHERE ( a.is_active=1 And a.is_publish=1 ) AND'
      sql=sql+'(a.title LIKE %(title)s  OR  a.description LIKE %(description)s ) OR '
      sql=sql+'(a.auto_type LIKE %(auto_type)s  OR  a.year LIKE %(year)s ) OR '
      sql=sql+'(a.color LIKE %(color)s  OR  a.fuel_type LIKE %(fuel_type)s ) OR '
      sql=sql+'(a.body_condition LIKE %(body_condition)s  OR  a.inside_out LIKE %(inside_out)s ) OR '
      sql=sql+'(a.transmission_type LIKE %(transmission_type)s  OR  a.door LIKE %(door)s ) OR '
      sql=sql+'(a.power LIKE %(power)s  OR  a.specs LIKE %(specs)s ) OR '
      sql=sql+'(a.cylinders LIKE %(cylinders)s  OR  a.streeingside LIKE %(streeingside)s ) '

      if len(brands)!=0 :
        sql=sql+ 'OR a.brand_id IN %(brand_id)s '
      if len(brandmodels)!=0 :
        sql=sql+ 'OR a.brandmodel_id IN %(brandmodels)s '
      if len(cats) !=0 :
        sql=sql+ 'OR  a.cat_id IN %(category_id)s  '
      if len(subcats)!=0 :
         sql=sql+ 'OR  a.subcat_id IN %(subcat)s '

      sql=sql+" ORDER BY a.id desc "
      params={"uid":uid,"title":'%'+pattern+'%',"description":'%'+pattern+'%','category_id':cats_id,'brand_id' :brands_id,
                "auto_type":'%'+pattern+'%',"year":'%'+pattern+'%',"color":'%'+pattern+'%',"fuel_type":'%'+pattern+'%',
                "body_condition":'%'+pattern+'%',"inside_out":'%'+pattern+'%',"transmission_type":'%'+pattern+'%'
                ,"door":'%'+pattern+'%',"power":'%'+pattern+'%',"specs":'%'+pattern+'%',"cylinders":'%'+pattern+'%'
                 ,"streeingside":'%'+pattern+'%',"brandmodels":brandmodels_id,"subcat":subcats_id
                }
      queryset = Automotive.objects.raw(sql,params)

      serializer=AutomotiveFavSerializer(queryset,many=True).data
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
  #def get(self,request):
  def post(self, request, format=None):
      uid=request.user.id
      category=request.data.get('category')
      brand=request.data.get('brand')
      brandmodel=request.data.get('brandmodel')
      subcat=request.data.get('subcat')
      country=request.data.get('country')
      state=request.data.get('state')
      city=request.data.get('city')
      auto_type=request.data.get('auto_type')
      transmission_type=request.data.get('transmission_type')
      fuel_type=request.data.get('fuel_type')
      color=request.data.get('color')
      door=request.data.get('door')
      power=request.data.get('power')
      specs=request.data.get('specs')
      cylinders=request.data.get('cylinders')
      streeingside=request.data.get('streeingside')
      maxprice=request.data.get('maxprice')
      minprice=request.data.get('minprice')
      currency=request.data.get('currency')
      year=request.data.get('year')
      body_condition=request.data.get('body_condition')
      inside_out=request.data.get('inside_out')

      sql='SELECT f.is_fav,a.id from automotive_automotive a left JOIN  automotive_automotivefave f on a.id = f.automotive_id '
      sql=sql+'AND f.uid_id=%(uid)s WHERE ( a.is_active=1 And a.is_publish=1 ) '
      if body_condition=="Select Body Condition" : body_condition=""
      if body_condition !="" :
        sql=sql+'And ( a.body_condition LIKE %(body_condition)s)'
      if inside_out =="Select Inside out": inside_out=""
      if inside_out !="" :
        sql=sql+'And ( a.inside_out LIKE %(inside_out)s)'
      if  specs=="Select Specs" : specs=""
      if specs !="" :
        sql=sql+'And ( a.specs LIKE %(specs)s)'
      if auto_type !="":
        sql=sql+'And ( a.auto_type LIKE %(auto_type)s)'
      if color =="Select Color": color=""
      if color !="" :
        sql=sql+'And ( a.color LIKE %(color)s)'
      if fuel_type !="" :
        sql=sql+'And ( a.fuel_type LIKE %(fuel_type)s)'
      if door=="Door Number" : door=""
      if door !="" :
        sql=sql+'And ( a.door LIKE %(door)s)'
      if power=="Select Power" : power=""
      if power !="" :
        sql=sql+'And ( a.power LIKE %(power)s)'
      if cylinders =="Select Cylinder" : cylinders=""
      if cylinders !="" :
        sql=sql+'And ( a.cylinders LIKE %(cylinders)s)'
      if transmission_type!="":
        sql=sql+'And ( a.transmission_type LIKE %(transmission_type)s)'
      if streeingside =="Select Side" :  streeingside=""
      if streeingside !="" :
        sql=sql+'And ( a.streeingside LIKE %(streeingside)s)'
      if maxprice !="" and minprice !="" :
       sql=sql+ 'And (a.price BETWEEN %(minprice)s AND %(maxprice)s)'
      if int(category) !=0:
        sql=sql+'And (a.cat_id = %(category_id)s)'
      if brand !="":
        sql=sql+'And (a.brand_id =%(brand_id)s)'
      if brandmodel !="" :
         sql=sql+'And (a.brandmodel_id =%(brandmodels)s)'
      if subcat !="" :
           sql=sql+'And (a.subcat_id =%(subcat)s)'

      if country !="":
        sql=sql+'And (a.country_id =%(country_id)s)'
      if state !="":
        sql=sql+'And (a.state_id =%(state_id)s)'
      if city !="":
        sql=sql+'And (a.city_id =%(city_id)s)'
      if year!="":
        sql=sql+'And (a.year LIKE %(year)s)'
      if currency!="":
        sql=sql+'And (a.currency LIKE %(currency)s)'

      sql=sql+" ORDER BY a.id desc "
      params={"uid":uid,'category_id':category,'brand_id' :brand,"brandmodels":brandmodel,"subcat":subcat,"maxprice":maxprice,"minprice":minprice,
                "auto_type":'%'+auto_type+'%',"year":'%'+year+'%',"color":'%'+color+'%',"fuel_type":'%'+fuel_type+'%',
               "transmission_type":'%'+transmission_type+'%',"currency":'%'+currency+'%',"inside_out":'%'+inside_out+'%',
                "body_condition":'%'+body_condition+'%',"door":'%'+door+'%',"power":'%'+power+'%',"specs":'%'+specs+'%',"cylinders":'%'+cylinders+'%'
                 ,"streeingside":'%'+streeingside+'%',"country_id":country,"state_id":state,"city_id":city,
                }

      queryset = Automotive.objects.raw(sql,params)
      serializer=AutomotiveFavSerializer(queryset,many=True).data
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

class ayman(APIView):
   def post(self, request, format=None):
      mystring="1,2,5,10"
      x = mystring.split(",")
      for y in x:
         print(y)
      return Response(x, status=status.HTTP_200_OK)

class MyAutomotiveApiView(APIView):
  permission_classes = [IsAuthenticated]
  def get(self,request,format=None):
    uid=request.user
    automotive= Automotive.objects.filter(uid=uid.id).order_by('-id')
    Countrpending= Automotive.objects.filter(uid=uid.id,is_publish=0,is_reject=0).count()
    Countreject= Automotive.objects.filter(uid=uid.id,is_reject=1).count()
    Countactive= Automotive.objects.filter(uid=uid.id,is_active=1,is_publish=1,is_reject=0).count()
    Countdisactive= Automotive.objects.filter(uid=uid.id,is_active=0,is_publish=1,is_reject=0).count()
    serializer = AutomotiveFavSerializer(automotive, many=True)
    counts=len(serializer.data)
    expected_data = {
          "count":counts,
          "active" : Countactive,
          "dis active":Countdisactive,
          "bending":Countrpending,
          "reject":Countreject,
          "My Automotive":serializer.data ,}
    json_data = {
      "code" : 200,
      "message" : "success",
      "data" :expected_data
      }
    return Response(json_data, status=status.HTTP_200_OK)
class MyAutomotiveActiveApiView(APIView):
  permission_classes = [IsAuthenticated]
  def get(self,request,format=None):
    uid=request.user
    automotive= Automotive.objects.filter(uid=uid.id,is_active=1,is_publish=1).order_by('-id')
    serializer = AutomotiveFavSerializer(automotive, many=True)
    counts=len(serializer.data)
    expected_data = {
           "count":counts,
            "My Automotive Active":serializer.data ,}
    json_data = {
      "code" : 200,
      "message" : "success",
      "data" :expected_data
      }
    return Response(json_data, status=status.HTTP_200_OK)
class MyAutomotiveDisActiveApiView(APIView):
  permission_classes = [IsAuthenticated]
  def get(self,request,format=None):
    uid=request.user
    automotive= Automotive.objects.filter(uid=uid.id,is_active=0,is_publish=1).order_by('-id')
    serializer = AutomotiveFavSerializer(automotive, many=True)
    counts=len(serializer.data)
    expected_data = {
           "count":counts,
            "My Automotive Dis Active":serializer.data ,}
    json_data = {
      "code" : 200,
      "message" : "success",
      "data" :expected_data
      }
    return Response(json_data, status=status.HTTP_200_OK)


class MyAutomotivePendingApiView(APIView):
   permission_classes = [IsAuthenticated]
   def get(self,request,format=None):
    uid=request.user
    automotive= Automotive.objects.filter(uid=uid.id,is_publish=0,is_active=1).order_by('-id')
    serializer = AutomotiveFavSerializer(automotive, many=True)
    counts=len(serializer.data)
    expected_data = {
           "count":counts,
            "My Automotive pending":serializer.data ,}
    json_data = {
      "code" : 200,
      "message" : "success",
      "data" :expected_data
      }
    return Response(json_data, status=status.HTTP_200_OK)

class MyAutomotiveRejectApiView(APIView):
  permission_classes = [IsAuthenticated]
  def get(self,request,format=None):
    uid=request.user
    automotive= Automotive.objects.filter(uid=uid.id,is_reject=1).order_by('-id')
    serializer = AutomotiveFavSerializer(automotive, many=True)
    counts=len(serializer.data)
    expected_data = {
           "count":counts,
            "My Automotive Reject":serializer.data ,}
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
            return automotiveimages.objects.get(id=img_id )
        except automotiveimages.DoesNotExist:
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
