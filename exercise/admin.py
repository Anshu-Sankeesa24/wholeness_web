from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(user_detail)
admin.site.register(user_login)
