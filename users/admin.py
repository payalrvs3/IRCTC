from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username','email','first_name','last_name','phone','irctc_id','is_verified']
    fieldsets = UserAdmin.fieldsets + (
        ('IRCTC Info', {'fields': ('phone','date_of_birth','gender','address','id_type','id_number','irctc_id','is_verified')}),
    )
