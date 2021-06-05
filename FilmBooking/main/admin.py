from django.contrib import admin

# Register your models here.

from . import models
 
admin.site.register(models.User)
admin.site.register(models.Admin)
admin.site.register(models.Movie)
admin.site.register(models.MovieTag)
admin.site.register(models.Cinema)
admin.site.register(models.Room)
admin.site.register(models.Schedule)
admin.site.register(models.Ticket)