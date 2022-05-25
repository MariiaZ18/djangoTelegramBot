from django.contrib import admin
from .models import University, Katedra, Subject,Files
# Register your models here.

@admin.register(University, Katedra, Subject, Files)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
