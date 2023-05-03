from rest_framework import serializers
from usersapp.models import User,Country,State,City
from jobs.models import Category,SubCategory,Skill,Eductation,Economicactivity,Company,Person,SocialWeb

class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','fullname','profile_image')
class CountryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id','country')
class StateNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('id','state')
class CityNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id','city')

class CategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name',)
class CategoryWebNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name','image')
        
class SubcatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'
class SubcatWebNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id','name','image')
class SubcatNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id','name',)

class CatDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = SubCategory
        fields = ('id', 'name',  'category')
class SkillsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        
class EductationsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eductation
        fields = '__all__'        
        
class EconomicactivityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Economicactivity
        fields = '__all__'  
class CompanysListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'  
class PersonsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'  

class SocialWebListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialWeb
        fields = '__all__'  



        
        