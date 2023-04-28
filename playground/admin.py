from django.contrib import admin
from .models import *


admin.site.register(TEST_Like_films)
admin.site.register(Cinemas)
admin.site.register(Films)
admin.site.site_url = "/playground/hello"
# Register your models here.
