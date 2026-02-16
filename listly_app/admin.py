from django.contrib import admin
from listly_app.models import listly_user, task



# Register your models here.
class data_display(admin.ModelAdmin) : 
    list_display = ("description", "completed", "created_at",)
admin.site.register(task, data_display)
admin.site.register(listly_user)