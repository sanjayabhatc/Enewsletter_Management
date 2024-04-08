from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Department, UserProfile, NewsLetter, Bookmark, Subscription

# Register your models here.
admin.site.register(Department)
admin.site.register(UserProfile)
admin.site.register(NewsLetter)
admin.site.register(Bookmark)
admin.site.register(Subscription)
