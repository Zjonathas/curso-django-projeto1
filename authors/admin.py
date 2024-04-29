from django.contrib import admin
from authors.models import Profile


@admin.register(Profile)
class ProfileAdminI(admin.ModelAdmin):
    ...
