from django.contrib import admin
from .models import User, Link, Click

# Register your models here.
admin.site.register(User)
admin.site.register(Link)
admin.site.register(Click)