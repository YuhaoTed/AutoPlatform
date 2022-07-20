from django.contrib import admin

# Register your models here.
from Automation import models
admin.site.register(models.UserAuto)
admin.site.register(models.Function)
admin.site.register(models.Project)
admin.site.register(models.Feature)
admin.site.register(models.Case)
admin.site.register(models.Case_Detail)
