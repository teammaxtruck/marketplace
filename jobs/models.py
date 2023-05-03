from django.db import models
from usersapp.models import User ,Country,State,City
from usersapp.handle_images import compress_image
import os

def upload_to_job(instance, filename):
    return 'images/job/{filename}'.format(filename=filename)
def upload_to_license_files(instance, filename):
    return 'images/job/company/license_files/{filename}'.format(filename=filename)
def upload_to_logos(instance, filename):
    return 'images/job/company/logos/{filename}'.format(filename=filename)
  
def upload_to_cv(instance, filename):
    return 'images/job/cv/{filename}'.format(filename=filename)
   
  

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(max_length=256, upload_to=upload_to_job, null=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return str(self.name)
    
class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='sub_category', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

class Economicactivity(models.Model):
    name = models.CharField(max_length=512, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Eductation(models.Model):
    name = models.CharField(max_length=200)
    is_deleted=models.BooleanField(default=False)

    def __str__(self):
        return self.name
class Skill(models.Model):
    name = models.CharField(max_length=200)
    is_deleted=models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Company(models.Model):
    uid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=512, null=True, blank=True)
    economicactivity = models.ForeignKey(Economicactivity, on_delete=models.CASCADE, null=True, blank=True)
    category= models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    subcategory= models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    license_file = models.FileField(null=True, blank=True,  upload_to=upload_to_license_files)
    logo = models.ImageField(max_length=255, null=True, blank=True, upload_to=upload_to_logos)
    cover_image = models.ImageField(max_length=255, null=True, blank=True, upload_to=upload_to_logos)
    website = models.CharField(max_length=512, null=True, blank=True)
    email = models.EmailField(max_length=256, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)

    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    address=models.CharField(max_length=512, null=True, blank=True)

    longitude = models.CharField(max_length=512, null=True, blank=True)
    latitude = models.CharField(max_length=512, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
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
             
            logo = self.logo
            cover_image=self.cover_image
            if logo and logo.size > (0.3 * 1024 * 1024):
                self.logo = compress_image(logo)
            if cover_image and cover_image.size > (0.3 * 1024 * 1024):
                self.cover_image = compress_image(cover_image)
            
            super(Company, self).save(*args, **kwargs)
           # super(, self).save(*args, **kwargs)
    def delete(self,*args,**kwargs):
        if os.path.isfile(self.cover_image.path):
            os.remove(self.cover_image.path)
        if os.path.isfile(self.logo.path):
            os.remove(self.logo.path)

        super(Company, self).delete(*args,**kwargs)

    # def save(self, *args, **kwargs):
    #     if self.logo:
    #         self.logo = s3_compress_image(self.logo)
    #     if self.cover_image:
    #         self.cover_image = s3_compress_image(self.cover_image)
    #     super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)




class Person(models.Model):

    uid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    firstname = models.CharField(max_length=512, null=True, blank=True)
    lastname = models.CharField(max_length=512, null=True, blank=True)
    sex = models.BooleanField(default=True) # true male False Fmale
    eductation = models.ForeignKey(Eductation, on_delete=models.CASCADE, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    website = models.CharField(max_length=512, null=True, blank=True)
    email = models.EmailField(max_length=256, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    cv = models.FileField(upload_to=upload_to_cv,null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    address=models.CharField(max_length=512, null=True, blank=True)
    longitude = models.CharField(max_length=512, null=True, blank=True)
    latitude = models.CharField(max_length=512, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)


    def delete(self,*args,**kwargs):
        if os.path.isfile(self.cv.path):
            os.remove(self.cv.path)
      

        super(Person(), self).delete(*args,**kwargs)

    def __str__(self):
        return str(self.lastname)

class SocialWeb(models.Model):
    SOCIALWEB_CHOICES = [
        ('Twitter', 'Twitter'),
        ('Facebook', 'Facebook'),
        ('Instagram ', 'Instagram '),
        ('linkedin', 'linkedin'),
        ('GitHub ','GitHub'),
        ('GitLab ','GitLab'),
        ('Website', 'Website'),

    ]
    uid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    person=models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200,choices=SOCIALWEB_CHOICES)
    link= models.CharField(max_length=200)
    is_deleted=models.BooleanField(default=False)


    def __str__(self):
        return self.name
class RecentJobs(models.Model):
    uid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    person=models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
    jobtitle=models.CharField(max_length=200)
    Employer=models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    address=models.CharField(max_length=512, null=True, blank=True)
    startdate=models.DateTimeField(null=True, blank=True)
    enddate=models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.jobtitle

class EducatJobs(models.Model):
    uid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    person=models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
    schoolname=models.CharField(max_length=200)
    schoollocation=models.CharField(max_length=200)
    educt=models.ForeignKey(Eductation, on_delete=models.SET_NULL, null=True, blank=True)
    fieldofstudy =models.CharField(max_length=200)
    startdate=models.DateTimeField(null=True, blank=True)
    enddate=models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.schoolname

class SkillsJobs(models.Model):
    uid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    person=models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
    skill=models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True)
    description=models.CharField(max_length=200)
    rate=models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)
