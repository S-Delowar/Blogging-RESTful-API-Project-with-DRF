from django.contrib import admin

from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", 
                    "author", 
                    "created_at", 
                    "updated_at",
                    )

admin.site.register(Post, PostAdmin)