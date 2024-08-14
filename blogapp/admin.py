from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class ArchiveAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['title',  'author', 'created_on', 'section', 'main_post']
    list_editable = ['section', 'main_post']
    list_filter = ("section",)
    search_fields = ['title', 'content']

admin.site.register(Contact)
admin.site.register(Profile)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)