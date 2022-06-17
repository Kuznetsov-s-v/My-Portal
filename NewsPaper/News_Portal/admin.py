
# Register your models here.
from django.contrib import admin
from .models import Category, Author, Post, Comment, PostCategory


admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostCategory)
