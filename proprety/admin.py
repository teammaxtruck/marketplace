from django.contrib import admin
from proprety.models import Category,SubCategory,proprety,propretyimages
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
      list_display = ('id','name',)
      list_per_page=10
      search_fields = ('name',)
      ordering = ('name','id')
      filter_horizontal = ()
      
class SubCategoryAdmin(admin.ModelAdmin):
  
     list_display = ('id','name','category',)
     list_filter = ('category',)
     list_per_page=10
     search_fields = ('name','category')
     ordering = ('name','id')
     filter_horizontal = ()
class PropretyImageInline(admin.TabularInline):
    model = propretyimages
    fields = ['proprety','proprety_image','is_main']
    list_display=['proprety_image','is_main']
    extra = 1
class PropretyModelAdmin(admin.ModelAdmin):
    list_display = ('id','uid','title','prop_type','category','subcategory','is_active','is_publish','is_reject')
    list_filter = ('category','is_active','is_publish','is_reject')
    inlines = [PropretyImageInline]
    list_per_page=10
  
    ordering = ('category','id')
    filter_horizontal = ()

admin.site.register(Category,CategoryAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(proprety,PropretyModelAdmin)
