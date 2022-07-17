from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Operator


class OperatorModelAdmin(admin.ModelAdmin):
    list_display = ('operator_name', 'id', 'is_delete')


admin.site.register(User, UserAdmin)
admin.site.register(Operator, OperatorModelAdmin)
