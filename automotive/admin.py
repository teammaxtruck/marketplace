from django.contrib import admin
from automotive.models import Brands,BrandModels,Categories,Subcatgoriess ,Automotive,automotiveimages



class CategoryAdmin(admin.ModelAdmin):
      list_display = ('id','name','image','is_home')
      list_filter = ('is_home',)
      list_per_page=10
      search_fields = ('name',)
      ordering = ('name','id')
      filter_horizontal = ()
      
class SubCategoryAdmin(admin.ModelAdmin):
  
     list_display = ('id','name','cat','image')
     list_filter = ('cat',)
     list_per_page=10
      #search_fields = ('name','cat')
     ordering = ('name','id')
     filter_horizontal = ()
      
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id','name','cat','is_home','image')
    list_filter = ('cat','is_home')
    list_per_page=10

    search_fields = ('name',)
    ordering = ('name','id')
    filter_horizontal = ()

class BrandModelAdmin(admin.ModelAdmin):
    list_display = ('id','name','brand')
    list_filter = ('brand',)
    list_per_page=10
  
    ordering = ('name','id')
    filter_horizontal = ()

class AutomotiveImageInline(admin.TabularInline):
    model = automotiveimages
    fields = ['automotive','automotive_image','is_main']
    list_display=['automotive_image','is_main']
    extra = 1
class AutomotiveModelAdmin(admin.ModelAdmin):
    list_display = ('id','uid','title','auto_type','cat','subcat','brand','brandmodel','is_active','is_publish','is_reject')
    list_filter = ('brand','cat','is_active')
    inlines = [AutomotiveImageInline]
    list_per_page=10
  
    ordering = ('cat','id')
    filter_horizontal = ()

# Register your models here..
admin.site.register(Categories,CategoryAdmin)
admin.site.register(Subcatgoriess,SubCategoryAdmin)

admin.site.register(Brands,BrandAdmin)
admin.site.register(BrandModels,BrandModelAdmin)
admin.site.register(Automotive,AutomotiveModelAdmin)
# Register your models here.
