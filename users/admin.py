from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class SarafanAdminUser(admin.ModelAdmin):
    search_fields = ('first_name', 'email')


admin.site.register(User, SarafanAdminUser)
