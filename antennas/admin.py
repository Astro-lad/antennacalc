from django.contrib import admin
from .models import Antenna

@admin.register(Antenna)
class YagiAdmin(admin.ModelAdmin):
    list_display = ['name', 'image']

