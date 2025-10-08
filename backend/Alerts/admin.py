from django.contrib import admin
from .models import Alert, SMS

# Register your models here.
admin.site.register(Alert)
admin.site.register(SMS)