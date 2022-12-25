from django.contrib import admin
from .models import Post, Category, PostImage, HashTag


class PostImageAdmin(admin.StackedInline):
    model = PostImage


class PostHashTagAdmin(admin.StackedInline):
    model = HashTag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'status', 'request_date', 'publication_date')
    list_display_links = ('title',)
    inlines = [PostImageAdmin, PostHashTagAdmin]

    class Meta:
        model = Post


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'post')
    list_display_links = ('post',)


@admin.register(HashTag)
class HashTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'post')
    list_display_links = ('name', 'post')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
