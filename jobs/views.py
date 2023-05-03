from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.pagination import  PageNumberPagination
from django.shortcuts import get_object_or_404

from rest_framework import status,generics
from jobs.serializers import (CategoryNameSerializer,CategoryWebNameSerializer, SubcatListSerializer,
                                 )
from jobs.models import (Category,SubCategory,)

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
    
