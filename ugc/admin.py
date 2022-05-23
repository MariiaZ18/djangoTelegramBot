from django.contrib import admin
from .models import University, Katedra, Subject
# Register your models here.

@admin.register(University, Katedra, Subject)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
