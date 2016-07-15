from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import  UserProfile
from .models import Project, Review

# Registering User Profile Models .
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserProfileAdmin(UserAdmin):
    inlines=(UserProfileInline, )
	
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'location', 'type'] 
    search_fields = ['user']

admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserProfileAdmin)

admin.site.register(UserProfile, ProfileAdmin)

# Registering GitHub Models .
	
class RepoAdmin(admin.ModelAdmin):
    model = Project
    list_display = ('id', 'url', 'owner_id', 'name', 'description', 'language', 'created_at', 'updated_at')
    search_fields = ['name','owner_id', 'language']
#    prepopulated_fields = {"slug": ("name",)}	
#    date_hierarchy = 'created_at'
    ordering = ['name','owner_id']

admin.site.register(Project, RepoAdmin)

# Registering Review Models .
	
class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('repo', 'title', 'rating', 'user_name', 'comment', 'pub_date')
    list_filter = ['pub_date', 'user_name']
    search_fields = ['title', 'user_name']
    raw_id_fields = ('user_name',)
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'pub_date'
    ordering = ['rating', 'pub_date']	

admin.site.register(Review, ReviewAdmin)

