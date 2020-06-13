from django.contrib import admin

from .models import Post, Comment, PostCategory


# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(PostCategory)
class PostCategory(admin.ModelAdmin):
    list_display = ('title', 'slug', 'approve', 'created', 'updated')
    list_filter = ('approve', 'created', 'updated')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Comment)
# admin.site.register(PostCategory)
