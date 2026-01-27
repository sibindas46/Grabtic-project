from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.Place)

admin.site.register(models.Theatre)

admin.site.register(models.Screens)

admin.site.register(models.ShowDate)

admin.site.register(models.ShowTime)

admin.site.register(models.OngoingShows)

admin.site.register(models.ScreensDateTime)

admin.site.register(models.Seat)

admin.site.register(models.Bookings)


