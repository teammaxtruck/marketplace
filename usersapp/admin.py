from django.contrib import admin
from usersapp.models import User,Language,Keylang
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
class UserModelAdmin(BaseUserAdmin):
 
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    #   
    list_display = ('id','is_active','email','fullname','phone','code','country','state','city','profile_image','type_user','is_admin')
    list_filter = ('is_admin','type_user')
    list_per_page=10

    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('is_active','fullname','phone','code','country','state','city','profile_image','type_user')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullname','phone','code','country','state','city','type_user','profile_image', 'password1', 'password2'),
        }),
    )
    search_fields = ('email','fullname')
    ordering = ('email','id')
    filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)

class KeylangModelAdmin(admin.ModelAdmin):
    list_display = ('id','lang','key','value')
    list_filter = ('lang',)
    search_fields = ('key','value')

    list_per_page=10
  
    ordering = ('lang','id')
    filter_horizontal = ()


admin.site.register(Keylang,KeylangModelAdmin)

admin.site.register(Language)