from django.contrib import admin

from .models import Trip, User

admin.site.register(User)
admin.site.register(Trip)
