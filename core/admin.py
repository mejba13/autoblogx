from django.contrib import admin
from .models import Post, Media, SEOMeta

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Media)
admin.site.register(SEOMeta)
