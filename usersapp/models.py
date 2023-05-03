from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from usersapp.handle_images import compress_image
from asgiref.sync import async_to_sync

def upload_to(instance, filename):
    
    return 'images/products/{filename}'.format(filename=filename)

def upload_to_u(instance, filename):
    
    return 'images/users/{filename}'.format(filename=filename)    

#---
class Language(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=5)

  
    def __str__(self):
        return f"{self.name} - {self.code}"
class Keylang(models.Model):
    lang=models.ForeignKey(Language, blank=False, related_name='lang',on_delete=models.CASCADE,default=1)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.key} - {self.value}"
  

class Country(models.Model):
    country = models.CharField(max_length=50,blank=False,default=1)
    code = models.CharField(max_length=5,blank=False,default=1)
    currency = models.CharField(max_length=5,blank=False,default=1)
    currency_name = models.CharField(max_length=50,blank=False,default=1)
    currency_symbol=models.CharField(max_length=5,blank=False,default=1)

    def __str__(self):
        return self.country


class State(models.Model):
    country = models.ForeignKey(Country, blank=False, related_name='country_state',on_delete=models.CASCADE,default=1)
    state = models.CharField(max_length=50,default="state")

    def __str__(self):
        return self.state


class City(models.Model):
    country = models.ForeignKey(Country, blank=False,related_name='country_city', on_delete=models.CASCADE,default=1)
    state = models.ForeignKey(State, blank=False, on_delete=models.CASCADE,default=1)
    city = models.CharField(max_length=50,default="city")

    def __str__(self):
        return self.city

#   ---------------------------------

class UserManager(BaseUserManager):
    

    def create_user(self, email,fullname,phone,code,country,state,city,type_user, password=None,password2=None):
        """
        Creates and saves a User with the given email, name,tc and password.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            fullname=fullname,
            phone=phone,
            code=code,
            type_user=type_user,
            country=country,
            state=state,
            city=city,
           
        )
        
        user.set_password(password)
        user.save(using=self._db)
       
        return user
    

    def create_superuser(self, email,fullname,phone,code,country,state,city,type_user, password=None):
        """
        Creates and saves a superuser with the given email, name,tc, and password.
        """
        user = self.create_user(
            email,
            password=password,
            fullname=fullname,
            phone=phone,
            code=code,
            type_user=type_user,
            country=country,
            state=state,
            city=city,
             
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


#Custom User Model
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    fullname=models.CharField(max_length=200)
    profile_image= models.ImageField(upload_to=upload_to_u, blank=True, null=True,default='images/users/person.png')
    bg_image= models.ImageField(upload_to=upload_to_u, blank=True, null=True,default='images/users/grid.png')
    type_user=models.IntegerField(blank=True, null=True,default=1) # 1 company 2 person
    phone=models.CharField(max_length=200)
    code=models.CharField(max_length=5,default='+000')
    country= models.ForeignKey(Country,on_delete=models.CASCADE,related_name='country_user',default=194)
    state= models.ForeignKey(State,on_delete=models.CASCADE,related_name='state_user',default=2849)
    city= models.ForeignKey(City,on_delete=models.CASCADE,related_name='city_user',default=102874)
    is_active = models.BooleanField(default=True)
    is_publish = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    user_token=models.CharField(max_length=250)
    
     # if size greater than 300kb then it will send to compress image function
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
        profile_image = self.profile_image
        if profile_image and profile_image.size > (0.3 * 1024 * 1024):
            self.profile_image = compress_image(profile_image)

        bg_image = self.bg_image
        if bg_image and bg_image.size > (0.3 * 1024 * 1024):
            self.bg_image = compress_image(bg_image)
      
        super(User, self).save(*args, **kwargs)
    
        

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname','phone','code','country','state','city','type_user']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
   