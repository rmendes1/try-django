from django.contrib import admin
from .models import Article
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'timestamp', 'updated', 'publish']
    search_fields = ['title', 'content']


admin.site.register(Article, ArticleAdmin)
