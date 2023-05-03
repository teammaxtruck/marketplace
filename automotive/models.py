from django.db import models
from usersapp.models import User ,Country,State,City
from usersapp.handle_images import compress_image
# Create your models here.
from datetime import date
def upload_to_b(instance, filename):
    return 'images/brands/{filename}'.format(filename=filename)
def upload_to_c(instance, filename):
    return 'images/cats/{filename}'.format(filename=filename)
def upload_to_Auto(instance, filename):
    return 'images/automotive/{filename}'.format(filename=filename)

     
class Categories(models.Model):
    name = models.CharField(max_length=100,unique=True)
    image = models.ImageField(upload_to=upload_to_c, blank=True, null=True)
    is_home = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

     
    def __str__(self):
        return self.name
  
class Subcatgoriess(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_to_c, blank=True, null=True)
    cat = models.ForeignKey(Categories, on_delete=models.CASCADE,default=1,related_name='subcat')
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['cat']
    def __str__(self):
        return self.name
    
class Brands(models.Model):
    name = models.CharField(max_length=100,unique=False)
    image = models.ImageField(upload_to=upload_to_b, blank=True, null=True)
    cat = models.ForeignKey(Categories, on_delete=models.CASCADE,default=1)
    is_home= models.BooleanField(default=False)
    is_deleted =models.BooleanField(default=False)

    staticmethod

    def __str__(self):
        return self.name
    
    def get_all_brands():
        return Brands.objects.all()

class BrandModels(models.Model):
    name = models.CharField(max_length=100,unique=False)
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE,default=1,related_name='brandmodel')
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
    def get_all_brandmodelss():
        return BrandModels.objects.all()
    

class Automotive(models.Model):

 
    CAR_TYPE_CHOICES = [
        ('New', 'New'),
        ('Used', 'Used'),
    ]
    FUEL_TYPE_CHOICES = [
        ('Gasoline', 'Gasoline'),
        ('Diesel', 'Diesel'),
        ('Hybrid', 'Hybrid'),
        ('Electric', 'Electric'),
    ]
    DOOR_CHOICES = [
        ('2 doors', '2 doors'),
        ('3 doors', '3 doors'),
        ('4 doors', '4 doors'),
        ('5+ doors', '5+ doors'),
    ]
    STREEING_SIDE_CHOICES = [
        ('Left Hand Side', 'Left Hand Side'),
        ('Right Hand Side', 'Right Hand Side'),
    ]
    SPECS_CHOICES = [
        ('European Specs', 'European Specs'),
        ('GCC Specs', 'GCC Specs'),
        ('Japanese Specs', 'Japanese Specs'),
        ('North American Specs', 'North American Specs'),
        ('Other', 'Other'),
    ]
    
    POWER_CHOICES = [
        ('Less than 150 HP', 'Less than 150 HP'),
        ('150- 200 HP', '150- 200 HP'),
        ('200- 300 HP', '200- 300 HP'),
        ('300- 400 HP', '300- 400 HP'),
        ('400- 500 HP', '400- 500 HP'),
        ('Other', 'Other')
    ]
    TRANSMISSION_TYPE_CHOICES = [
        ('Manual Transmission', 'Manual Transmission'),
        ('Automatic Transmission', 'Automatic Transmission'),
    ]
    BODY_CONDITION_CHOICES = [
        ('Perfect Inside and Outside', 'Perfect Inside and Outside'),
        ('No accidents, very few faults', 'No accidents, very few faults'),
        ('Bit of wear tear, all repaired', 'Bit of wear tear, all repaired'),
        ('Lots of wear tear to the body', 'Lots of wear tear to the body'),
    ]
    INSIDE_OUT_CHOICES = [
        ('Perfect Inside and Outside', 'Perfect Inside and Outside'),
        ('Minor faults, all fixed', 'Minor faults, all fixed'),
        ('Major faults fixed, small remains', 'Major faults fixed, small remains'),
        ('Ongoing minor major faults', 'Ongoing minor major faults'),
    ]

    uid= models.ForeignKey(User,on_delete=models.CASCADE,default=1 ,related_name='user')
    title = models.CharField(max_length=125,null=True, blank=True)
    auto_type = models.CharField(max_length=4, null=True, blank=True, choices=CAR_TYPE_CHOICES)
  
    year = models.CharField(max_length=10, null=True, blank=True)
    kilometers = models.CharField(max_length=10,null=True, blank=True)
    color = models.CharField(max_length=125, null=True, blank=True)
    fuel_type = models.CharField(max_length=125, null=True, blank=True, choices=FUEL_TYPE_CHOICES)
    body_condition = models.CharField(max_length=255, null=True, blank=True, choices=BODY_CONDITION_CHOICES)
    inside_out = models.CharField(max_length=255, null=True, blank=True, choices=INSIDE_OUT_CHOICES)


    cat=models.ForeignKey(Categories,on_delete=models.CASCADE,default=1 ,related_name='automotive_cat')
    subcat=models.ForeignKey(Subcatgoriess,on_delete=models.CASCADE,default=1 ,related_name='automotive_subcat')
    brand=models.ForeignKey(Brands,on_delete=models.CASCADE,default=1 ,related_name='automotive_brand')
    brandmodel=models.ForeignKey(BrandModels,on_delete=models.CASCADE,default=1 ,related_name='automotive_brandmodel')

    country=models.ForeignKey(Country,on_delete=models.CASCADE,default=1 ,related_name='automotive_country')
    state=models.ForeignKey(State,on_delete=models.CASCADE,default=1 ,related_name='automotive_state')
    city=models.ForeignKey(City,on_delete=models.CASCADE,default=1 ,related_name='automotive_city')
    code= models.CharField(max_length=15, null=True, blank=True)
    phone= models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency =models.CharField(max_length=15, null=True, blank=True)
   
    is_active = models.BooleanField(default=False)
    is_reject = models.BooleanField(default=False)
    is_publish=  models.BooleanField(default=True)

   ###for Cars
    transmission_type = models.CharField(max_length=64, null=True, blank=True, choices=TRANSMISSION_TYPE_CHOICES)
    door = models.CharField(max_length=64, null=True, blank=True, choices=DOOR_CHOICES)
    power = models.CharField(max_length=64, null=True, blank=True, choices=POWER_CHOICES)
    specs = models.CharField(max_length=64, null=True, blank=True, choices=SPECS_CHOICES)
    cylinders = models.CharField(max_length=64, null=True, blank=True)
    streeingside= models.CharField(max_length=64, null=True, blank=True, choices=STREEING_SIDE_CHOICES)
    #####
   
    is_promoted = models.BooleanField(default=False) # not owner
    description = models.TextField(null=True, blank=True)

    linkurl= models.CharField(max_length=250, null=True, blank=True)
    view   = models.IntegerField(null=True, blank=True,default=1)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

import os
class automotiveimages(models.Model):
    automotive = models.ForeignKey(Automotive, on_delete=models.CASCADE, null=True, blank=True, related_name='automotive_image')
    automotive_image = models.ImageField(max_length=256, upload_to=upload_to_Auto, null=True)
    is_main = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
            *args,
            **kwargs,
        ):
            # if size greater than 300kb then it will send to compress image function
             
            automotive_image = self.automotive_image
            if automotive_image and automotive_image.size > (0.3 * 1024 * 1024):
                self.automotive_image = compress_image(automotive_image)
            
            super(automotiveimages, self).save(*args, **kwargs)
           # super(, self).save(*args, **kwargs)
    def delete(self,*args,**kwargs):
        if os.path.isfile(self.automotive_image.path):
            os.remove(self.automotive_image.path)

        super(automotiveimages, self).delete(*args,**kwargs)

class automotivefave(models.Model):
    uid= models.ForeignKey(User,on_delete=models.CASCADE,default=1 ,related_name='automotive_user')
    automotive = models.ForeignKey(Automotive, on_delete=models.CASCADE, null=True, blank=True, related_name='automotive_fav')
    is_fav=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


####filter ads where country state city
class countryautomotiveads(models.Model):
    uid= models.ForeignKey(User,on_delete=models.CASCADE,default=1 ,related_name='automotiveads1_user')
    automotive = models.ForeignKey(Automotive, on_delete=models.CASCADE, null=True, blank=True, related_name='automotive1_ads')
    listcountry=models.CharField(max_length=250, null=True, blank=True)
    liststate=models.CharField(max_length=250, null=True, blank=True)
    listcity=models.CharField(max_length=250, null=True, blank=True)
'''

class automotiveads(models.Model):
    uid= models.ForeignKey(User,on_delete=models.CASCADE,default=1 ,related_name='ads_user')
    automotive = models.ForeignKey(Automotive, on_delete=models.CASCADE, null=True, blank=True, related_name='ads_automotive')
    location=models.IntegerField(default=0, blank=True, editable=False) # idcountry idstate idcity
    type_locaction=models.IntegerField(default=0, blank=True, editable=False) # 1 country 2 state 3 city
''' 


