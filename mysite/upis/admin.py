from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.

class korisniciAdmin(admin.ModelAdmin):
    fields = ['username','password','email','uloga','status']

admin.site.register(models.Korisnici, korisniciAdmin)
admin.site.register(models.Predmeti)
admin.site.register(models.Upisi)
admin.site.register(models.Uloga)