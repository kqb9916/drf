from django.contrib import admin

from api import models

admin.site.register(models.Student)
admin.site.register(models.Employee)