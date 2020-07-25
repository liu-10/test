from django.contrib import admin
from user.models import User, Address
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'create_time', 'update_time', 'is_active']


class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'receiver', 'address', 'phone']


admin.site.register(User, UserAdmin)
admin.site.register(Address, AddressAdmin)