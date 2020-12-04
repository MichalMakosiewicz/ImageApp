from django.contrib import admin
from .models import UserPlan, Image, UserProfile

admin.site.register(UserProfile)
admin.site.register(UserPlan)
admin.site.register(Image)