from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from gateway.models import User

class UserAdmin(UserAdmin):
    list_display = ('username', 'email','date_join','last_login','is_admin','is_staff')
    search_fields = ('username','email')
    readonly_fields=('date_join','last_login')

    filter_horizontal=()
    list_filter=()
    fieldsets=()

admin.site.register(User, UserAdmin)