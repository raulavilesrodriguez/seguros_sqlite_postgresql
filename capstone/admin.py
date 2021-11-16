from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User, Contact, PlanSeguro, Customer

# Register your models here.
class CustomUserAdmin(UserAdmin):    
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'last_login']

class ContacAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'timestamp', 'creador', 'iscustomer')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Contact, ContacAdmin)
admin.site.register(PlanSeguro)
admin.site.register(Customer)