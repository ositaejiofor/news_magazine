from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Article, BreakingNews, Comment


class ImagePreviewMixin:
    """Reusable mixin to show image thumbnails in admin list and detail views."""

    def thumbnail(self, obj):
        if hasattr(obj, "image") and obj.image:
            return format_html(
                '<img src="{}" width="60" height="40" style="object-fit:cover; border-radius:4px;" />',
                obj.image.url,
            )
        elif hasattr(obj, "featured_image") and obj.featured_image:
            return format_html(
                '<img src="{}" width="60" height="40" style="object-fit:cover; border-radius:4px;" />',
                obj.featured_image.url,
            )
        return "—"
    thumbnail.short_description = "Image"


# ------------------- CATEGORY -------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at", "updated_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


# ------------------- TAG -------------------
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at", "updated_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


# ------------------- COMMENT (INLINE) -------------------
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ("user", "content", "created_at")
    readonly_fields = ("created_at",)


# ------------------- ARTICLE -------------------
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin, ImagePreviewMixin):
    list_display = (
        "title", "author", "category", "status",
        "created_at", "updated_at", "thumbnail"
    )
    search_fields = ("title", "author__username", "category__name", "content")
    list_filter = ("status", "category", "author")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at", "image_preview")
    ordering = ("-created_at", "-updated_at")
    inlines = [CommentInline]

    def image_preview(self, obj):
        """Inline preview for the detail view"""
        if obj.featured_image:
            return format_html('<img src="{}" width="300" style="border-radius:6px;" />', obj.featured_image.url)
        return "No image"
    image_preview.short_description = "Featured Image Preview"


# ------------------- BREAKING NEWS -------------------
@admin.register(BreakingNews)
class BreakingNewsAdmin(admin.ModelAdmin, ImagePreviewMixin):
    list_display = ("headline", "active", "created_at", "updated_at", "thumbnail")
    search_fields = ("headline",)
    list_filter = ("active",)
    prepopulated_fields = {"slug": ("headline",)}
    readonly_fields = ("created_at", "updated_at", "image_preview")
    ordering = ("-created_at", "-updated_at")

    def image_preview(self, obj):
        """Inline preview for the detail view"""
        if obj.image:
            return format_html('<img src="{}" width="300" style="border-radius:6px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Image Preview"


# ------------------- COMMENT (DIRECT) -------------------
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "article", "is_reply", "created_at")
    search_fields = ("user__username", "article__title", "content")
    list_filter = ("created_at", "article")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
