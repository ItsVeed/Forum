from django.contrib import admin
from .models import Section, Category, Post, Comment
from django.utils.translation import gettext_lazy as _

admin.site.register(Section)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("comment", "post", "datetimeuploaded", "user")}),
        (
            _("Likes"),
            {
                "fields": (
                    "likes",
                )
            }
        )
    )
    list_display = ("user", "post", "datetimeuploaded")
    list_filter = ("user", "datetimeuploaded")
    search_fields = ("user", "post")
    readonly_fields=('datetimeuploaded', 'likes')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("title", "post", "datetimeuploaded", "user", 'category')}),
        (
            _("Likes"),
            {
                "fields": (
                    'likes',
                )
            }
        )
    )
    list_display = ("title", "user", "category", "datetimeuploaded")
    list_filter = ("user", "datetimeuploaded")
    search_fields = ("user__username", "category__name", "title")
    readonly_fields =('datetimeuploaded', 'likes')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("name", "order", "section")}),
        (
            _("Roles"),
            {
                "fields": (
                    "allowed_roles",
                )
            }
        )
    )
    filter_horizontal = ("allowed_roles",)