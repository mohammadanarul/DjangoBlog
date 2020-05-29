from django.contrib import admin
from .models import author, category, article, Comment

# Register your models here.
class authorModel(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ['__str__', 'details']
    list_per_page = 10
    class Meta:
        model = author

admin.site.register(author, authorModel)

class articleModel(admin.ModelAdmin):
    list_display  = ['__str__', 'posted_on', 'blog_post_views']
    search_fields = ['__str__', 'details']
    list_per_page = 10
    list_filter  = ['posted_on', 'category']
    class Meta:
        model = article
admin.site.register(article, articleModel)

class categoryModel(admin.ModelAdmin):
    list_display  = ['__str__']
    search_fields = ['__str__']
    list_per_page = 10

    class Meta:
        model = category

admin.site.register(category, categoryModel)

@admin.register(Comment)
class commentmodel(admin.ModelAdmin):
    list_display  = ['__str__', 'timestamp', ]
    list_filter   = ['user']
    search_fields = ['email', 'post_comment']
    list_per_page = 10
    class Meta:
        model = Comment

# admin.site.register(Comment, commentmodel)
