from rest_framework import serializers
from usersapp.models import User,Country,State,City
from automotive.models import Categories,Subcatgoriess,Brands,BrandModels,Automotive,automotiveimages,automotivefave
from usersapp.serializers import CitySerializer,CountrySerializer,StateSerializer


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
class BrandHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = ('id','name','image','is_home')
       
class BrandNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = ('id','name',)

class BrandModelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandModels
        fields = '__all__'
class BrandModelNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandModels
        fields = ('id','name',)
class CategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('id','name',)
class CategoryWebNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('id','name','image')
               
class SubcatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcatgoriess
        fields = '__all__'
class SubcatNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcatgoriess
        fields = ('id','name',)

class CatDetailSerializer(serializers.ModelSerializer):
    cat = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Subcatgoriess
        fields = ('id', 'name',  'cats','image')
class ImagesSerializer(serializers.ModelSerializer):
  class Meta:
    model =automotiveimages
    fields = ("id", "automotive_image","is_main", "automotive")
class FavoritSerializer(serializers.ModelSerializer):
  class Meta:
    model=automotivefave
    fields=("automotive","uid","is_fav")  
    
class AutomotiveSerializer(serializers.ModelSerializer):    
      
     class Meta:
        model = Automotive
        fields = '__all__'

class AutomotiveFavSerializer(serializers.ModelSerializer):
      
      automotive_image =ImagesSerializer(many=True)
      automotive_fav = FavoritSerializer(many=True)
      country=serializers.SlugRelatedField(many=False, slug_field="country",queryset=Country.objects.all())
      state=serializers.SlugRelatedField(many=False, slug_field="state",queryset=State.objects.all())
      city=serializers.SlugRelatedField(many=False, slug_field="city",queryset=City.objects.all())
      automotive_fav = serializers.IntegerField(source='automotive_fav.count',  read_only=True)
      price = serializers.SerializerMethodField()
      view= serializers.SerializerMethodField()
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
        
      def get_view(self, obj):
        if  obj.view <1000 :
             view=str(obj.view)
             return view
        if  obj.view >=1000 and   obj.view <1000000:
                view= "%.2f" % (obj.view/1000)
                view=str(view)+"K"
                return view

        if obj.view >=1000000 :
                view="%.2f" % (obj.view/1000000)
                view=str(view)+"M"
                return view     
      class Meta:
        model = Automotive
        fields = ('id','view' ,'title','auto_type','price','currency',
                  'country','state','city','automotive_image','automotive_fav')
        

class AutomotiveFav1Serializer(serializers.ModelSerializer):
      uid=UserNameSerializer(many=False)
      automotive_image =ImagesSerializer(many=True)
      automotive_fav = FavoritSerializer(many=True)
      brand=BrandNameSerializer(many=False)
      brandmodel=BrandModelNameSerializer(many=False)
      cat=CategoryNameSerializer(many=False)
      subcat=SubcatNameSerializer(many=False)

      automotive_fav = serializers.IntegerField(source='automotive_fav.count',  read_only=True)
      class Meta:
        model = Automotive
        fields = ('id','uid','title','auto_type','cat','subcat','brand','brandmodel', 'description','price','currency',
                  'year','kilometers','color','fuel_type','body_condition','inside_out','transmission_type','door',
                  'power','specs','cylinders','streeingside','linkurl','country','state','city','code','phone','address','automotive_image',
                  'created_at','updated_at','is_active','automotive_fav')
      
class AutomotiveDetalsSerializer(serializers.ModelSerializer):
    uid=UserNameSerializer(many=False)
    brand=BrandNameSerializer(many=False)
    brandmodel=BrandModelNameSerializer(many=False)
    cat=CategoryNameSerializer(many=False)
    subcat=SubcatNameSerializer(many=False)
    automotive_image =ImagesSerializer(many=True)     
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
        model = Automotive
        fields = ('id','uid',  'title','auto_type','cat','subcat','brand','brandmodel', 'description','price','currency',
                  'year','kilometers','color','fuel_type','body_condition','inside_out','transmission_type','door',
                  'power','specs','cylinders','streeingside','linkurl','code','phone','country','state','city','address','automotive_image',
                  'created_at','is_active')
        

'''

class AutomotiveAds(serializers.ModelSerializer):

  class Meta:
        model = automotiveads
        fields = '__all__'

'''