from django.contrib import admin

from .models import Category, Post, User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',),}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'create_date',)
    list_display_links = ('title',)
    list_filter = ('category', 'create_date', 'update_date',)
    search_fields = ('title', 'slug', 'description',)
    exclude = ['author',]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super().save_model(request, obj, form, change)


admin.site.register(User)
