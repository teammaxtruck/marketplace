from rest_framework import serializers
from usersapp.models import User,Country,State,City
from proprety.models import Category,SubCategory,proprety,propretyimages,propretyfave,propretyads

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

class ImagesSerializer(serializers.ModelSerializer):
  class Meta:
    model =propretyimages
    fields = ("id", "proprety_image","is_main", "proprety")
class FavoritSerializer(serializers.ModelSerializer):
  class Meta:
    model=propretyfave
    fields=("proprety","uid","is_fav")  
    
class propretySerializer(serializers.ModelSerializer):    
      
     class Meta:
        model = proprety
        fields = '__all__'

class propretyFavSerializer(serializers.ModelSerializer):
      
      proprety_image =ImagesSerializer(many=True)
      proprety_fav = FavoritSerializer(many=True)
      country=serializers.SlugRelatedField(many=False, slug_field="country",queryset=Country.objects.all())
      state=serializers.SlugRelatedField(many=False, slug_field="state",queryset=State.objects.all())
      city=serializers.SlugRelatedField(many=False, slug_field="city",queryset=City.objects.all())
      proprety_fav = serializers.IntegerField(source='proprety_fav.count',  read_only=True)
      price = serializers.SerializerMethodField()
      def get_price(self, obj):
        if  obj.price <1000 :
             price=str(obj.price)
             return price
        if  obj.price >=1000 and   obj.price <1000000:
                price=(obj.price/1000)
                price=str(price)+"K"
                return price

        if obj.price >=1000000 :
                price=obj.price/1000000
                price=str(price)+"M"
                return price
            
      class Meta:
        model = proprety
        fields = ('id','view' ,'title','prop_type','price','currency',
                  'country','state','city','proprety_image','proprety_fav')
        

class propretyFav1Serializer(serializers.ModelSerializer):
      uid=UserNameSerializer(many=False)
      proprety_image =ImagesSerializer(many=True)
      proprety_fav = FavoritSerializer(many=True)
      cat=CategoryNameSerializer(many=False)
      subcat=SubcatNameSerializer(many=False)
      proprety_fav = serializers.IntegerField(source='proprety_fav.count',  read_only=True)
      class Meta:
        model = proprety
        fields = ('id','uid', 'title','prop_type','category','subcategory', 'description','price','currency',
                  'area','areaunit','bedrooms','baths','description','furnished','living_room','balcony',
                  'lift','parking','storage','gym','cinema','conference','swimming_poll','maid_room','sports',
                  'country','state','city','address','linkurl','proprety_image',
                  'created_at','is_active','proprety_fav')
      
class propretyDetalsSerializer(serializers.ModelSerializer):
    uid=UserNameSerializer(many=False)
    category=CategoryNameSerializer(many=False)
    subcategory=SubcatNameSerializer(many=False)
    proprety_image =ImagesSerializer(many=True)     
    country=CountryNameSerializer(many=False)
    state=StateNameSerializer(many=False)
    city=CityNameSerializer(many=False)
    price = serializers.SerializerMethodField()
    def get_price(self, obj):
        if  obj.price <1000 :
             price=str(obj.price)
             return price
        if  obj.price >=1000 and  obj.price <1000000:
                price=(obj.price/1000)
                price=str(price)+"K"
                return price

        if obj.price >=1000000 :
                price=obj.price/1000000
                price=str(price)+"M"
                return price
    class Meta:
        model = proprety
        fields = ('id','uid', 'title','prop_type','category','subcategory', 'description','price','currency',
                  'area','areaunit','bedrooms','baths','description','furnished','living_room','balcony',
                  'lift','parking','storage','gym','cinema','conference','swimming_poll','maid_room','sports',
                  'country','state','city','address','linkurl','proprety_image',
                  'created_at','is_active')
        


class propretyAds(serializers.ModelSerializer):

  class Meta:
        model = propretyads
        fields = '__all__'