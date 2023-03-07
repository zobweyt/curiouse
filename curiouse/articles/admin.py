from django.contrib import admin

from .models import Author, Category, Article, Follow


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'follower', 'created_at')
    list_display_links = ('id',)
    search_fields = ('author', 'follower')
    list_filter = ('author', 'follower', 'created_at',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', '__str__', 'get_articles_count', 'get_followers_count')
    list_display_links = ('__str__',)
    search_fields = ('__str__',)
    
    @admin.display(description='Articles count')
    def get_articles_count(self, obj):
        return Article.objects.filter(author=obj).count()
    
    @admin.display(description='Followers count')
    def get_followers_count(self, obj):
        return obj.followers.count()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    list_display_links = ('title',)
    list_filter = ('categories', 'created_at', 'modified_at')
    search_fields = ('title', 'slug')
    exclude = ['author', 'slug']
    save_as = True

    def save_model(self, request, obj, form, change):
        obj.author = Author.objects.get(user=request.user)
        return super().save_model(request, obj, form, change)
