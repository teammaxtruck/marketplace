from django.contrib import admin
from jobs.models import Category,SubCategory,Skill,Eductation,Economicactivity,Company,Person
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

class SkillsAdmin(admin.ModelAdmin):
      list_display = ('id','name',)
      list_per_page=10
      search_fields = ('name',)
      ordering = ('name','id')
      filter_horizontal = ()
class EductationsAdmin(admin.ModelAdmin):
      list_display = ('id','name',)
      list_per_page=10
      search_fields = ('name',)
      ordering = ('name','id')
      filter_horizontal = ()

class EconomicactivityAdmin(admin.ModelAdmin):
      list_display = ('id','name',)
      list_per_page=10
      search_fields = ('name',)
      ordering = ('name','id')
      filter_horizontal = ()
                  
class CompanyModelAdmin(admin.ModelAdmin):
    list_display = ('id','uid','name','economicactivity','category','subcategory','email','phone','logo','cover_image','license_file')
    list_filter = ('economicactivity','category',)
    list_per_page=10
    search_fields = ('name','description','about')

    ordering = ('category','id')
    filter_horizontal = ()

class PersonModelAdmin(admin.ModelAdmin):
    list_display = ('id','uid','firstname','lastname','eductation','email','phone')
    list_filter = ('sex','eductation',)
    list_per_page=10
    search_fields = ('firstname','lastname','description','about')

    ordering = ('sex','id')
    filter_horizontal = ()


admin.site.register(Skill,SkillsAdmin)
admin.site.register(Eductation,EductationsAdmin)
admin.site.register(Economicactivity,EconomicactivityAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(Company,CompanyModelAdmin)
admin.site.register(Person,PersonModelAdmin)

# Register your models here.
