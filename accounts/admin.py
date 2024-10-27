from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm 
from . models import Profile


# Register your models here.
User = get_user_model()

class ProfileInline(admin.StackedInline):
    """
    Inline admin descriptor for Profile model.
    """

    model = Profile
    can_delete = False
    verbose_name_plural = "Profiles"



@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    inlines = (ProfileInline,)
    model = User
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active',)
    list_filter = ('email', 'username', 'last_name','is_staff', 'is_active',)
    search_fields = ('email', 'username','first_name', 'last_name',)
    ordering = ('email',)
    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = (
        "user",
        "profile_image",
        "bio",
        "phone_number",
        "website",
        "address",
        "date_of_birth",
    )
    search_fields = (
        "user__email",
        "user__username", 
        "phone_number", 
    )
    list_filter = ("user__date_of_birth",)