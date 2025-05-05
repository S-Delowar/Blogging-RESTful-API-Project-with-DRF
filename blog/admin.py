from django.contrib import admin

from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", 
                    "author", 
                    "created_at", 
                    "image",
                    )

admin.site.register(Post, PostAdmin)