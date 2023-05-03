from django.db import models
from usersapp.models import User ,Country,State,City
from usersapp.handle_images import compress_image
import os

def upload_to_Prop(instance, filename):
    return 'images/proprety/{filename}'.format(filename=filename)

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(max_length=256, upload_to=upload_to_Prop, null=True)
    is_deleted = models.BooleanField(default=False)

  
    def __str__(self):
        return str(self.name)
    
class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='sub_category', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

class proprety(models.Model):
     DATA_CHOICES = [
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4+', '4+'),
    ]
     TYPE_CHOICES = [
        ('Rent', 'Rent'),
        ('Sael', 'Sael'),
    ]
     UNIT_CHOICES=[
          ('Suqare Meter', 'Suqare Meter'),
          ('Suqare Feet', 'Suqare Feet'),
          ('Suqare Yard', 'Suqare Yard'),
          ('Kanal', 'Kanal'),
          ('Marla', 'Marla'),
         
     ]
     uid= models.ForeignKey(User,on_delete=models.CASCADE,default=1 ,related_name='user_p')
     title = models.CharField(max_length=125,null=True, blank=True)
     prop_type = models.CharField(max_length=4, null=True, blank=True, choices=TYPE_CHOICES)
     category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1 ,related_name='proprety_cat')
     subcategory=models.ForeignKey(SubCategory,on_delete=models.CASCADE,default=1 ,related_name='proprety_subcat')
     
     country=models.ForeignKey(Country,on_delete=models.CASCADE,default=1 ,related_name='proprety_country')
     state=models.ForeignKey(State,on_delete=models.CASCADE,default=1 ,related_name='proprety_state')
     city=models.ForeignKey(City,on_delete=models.CASCADE,default=1 ,related_name='proprety_city')
     code= models.CharField(max_length=15, null=True, blank=True)
     phone= models.CharField(max_length=15, null=True, blank=True)
     address = models.CharField(max_length=255, null=True, blank=True)

     price = models.DecimalField(max_digits=12, decimal_places=2)
     currency =models.CharField(max_length=15, null=True, blank=True)

     area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
     areaunit= models.CharField(max_length=255, choices=UNIT_CHOICES, null=True, blank=True)
     bedrooms = models.CharField(max_length=255, choices=DATA_CHOICES, null=True, blank=True)
     baths = models.CharField(max_length=255, choices=DATA_CHOICES, null=True, blank=True)
     description = models.TextField(null=True, blank=True)
     furnished= models.BooleanField(default=False)
     living_room = models.BooleanField(default=False)
     balcony =models.BooleanField(default=False)
     lift = models.BooleanField(default=False)
     parking =models.BooleanField(default=False)
     storage = models.BooleanField(default=False)
     gym = models.BooleanField(default=False)
     cinema = models.BooleanField(default=False)
     conference = models.BooleanField(default=False)
     swimming_poll = models.BooleanField(default=False)
     maid_room =models.BooleanField(default=False)
     sports = models.BooleanField(default=False)
     
     linkurl= models.CharField(max_length=250, null=True, blank=True)
     is_active =  models.BooleanField(default=False)
     is_reject = models.BooleanField(default=False)
     is_publish=  models.BooleanField(default=True)
     view   = models.IntegerField(null=True, blank=True,default=1)
     created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
     updated_at = models.DateTimeField(null=True, blank=True)
     is_deleted = models.BooleanField(default=False)

     

     def __str__(self):
        return str(self.title)
  
class propretyimages(models.Model):
    proprety = models.ForeignKey(proprety, on_delete=models.CASCADE, null=True, blank=True, related_name='proprety_image')
    proprety_image = models.ImageField(max_length=256, upload_to=upload_to_Prop, null=True)
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
             
            proprety_image = self.proprety_image
            if proprety_image and proprety_image.size > (0.3 * 1024 * 1024):
                self.proprety_image = compress_image(proprety_image)
            
            super(propretyimages, self).save(*args, **kwargs)
           # super(, self).save(*args, **kwargs)
    def delete(self,*args,**kwargs):
        if os.path.isfile(self.proprety_image.path):
            os.remove(self.proprety_image.path)

        super(propretyimages, self).delete(*args,**kwargs)

class propretyfave(models.Model):
    uid= models.ForeignKey(User,on_delete=models.CASCADE,default=1 ,related_name='proprety_user')
    proprety = models.ForeignKey(proprety, on_delete=models.CASCADE, null=True, blank=True, related_name='proprety_fav')
    is_fav=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


####filter ads where country state city
class countrypropretyads(models.Model):
    uid= models.ForeignKey(User,on_delete=models.CASCADE,default=1 ,related_name='propretyads1_user')
    proprety = models.ForeignKey(proprety, on_delete=models.CASCADE, null=True, blank=True, related_name='proprety1_ads')
    listcountry=models.CharField(max_length=250, null=True, blank=True)
    liststate=models.CharField(max_length=250, null=True, blank=True)
    listcity=models.CharField(max_length=250, null=True, blank=True)
    
class propretyads(models.Model):
    uid= models.ForeignKey(User,on_delete=models.CASCADE,default=1 ,related_name='pads_user')
    proprety = models.ForeignKey(proprety, on_delete=models.CASCADE, null=True, blank=True, related_name='ads_proprety')
    location=models.IntegerField(default=0, blank=True, editable=False) # idcountry idstate idcity
    type_locaction=models.IntegerField(default=0, blank=True, editable=False) # 1 country 2 state 3 city
    