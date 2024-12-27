from django.contrib import admin
from .models import RSVP

class RSVPAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "attending", "partner", "kids", "count_guests")

# Register your models here.
admin.site.register(RSVP)