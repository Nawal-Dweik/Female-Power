from django.contrib import admin

from .models import User, Profile, Comment, Post

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)