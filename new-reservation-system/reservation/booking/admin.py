from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(registeredUser)
admin.site.register(Date)
admin.site.register(Reservation)
admin.site.register(Table)