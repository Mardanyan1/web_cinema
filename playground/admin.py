from django.contrib import admin
from .models import Like_films


admin.site.register(Like_films)
admin.site.site_url = "/playground/hello"
# Register your models here.
