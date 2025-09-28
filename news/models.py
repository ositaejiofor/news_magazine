from django.db import models
from django.conf import settings
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User




STATUS = (
    (0,"Draft"),
    (1,"Publish")
)


# ==========================
# Base Model
# ==========================
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]


# ==========================
# Category
# ==========================
class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")

    class Meta(BaseModel.Meta):
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ==========================
# Tag
# ==========================
class Tag(BaseModel):
    name = models.CharField(max_length=30, unique=True, verbose_name="Tag Name")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    image = models.ImageField(upload_to='articles/', blank=True, null=True)


    class Meta(BaseModel.Meta):
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ==========================
# Article
# ==========================
class Article(BaseModel):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=200, verbose_name="Article Title")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="articles",
        verbose_name="Category",
    )
    tags = models.ManyToManyField(
        Tag, blank=True, related_name="articles", verbose_name="Tags"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="articles",
        verbose_name="Author",
    )
    content = RichTextUploadingField(verbose_name="Content")
    image = models.ImageField(
        upload_to="articles/", blank=True, null=True, verbose_name="Inline Image"
    )
    featured_image = models.ImageField(
        upload_to="articles/", blank=True, null=True, verbose_name="Featured Image"
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="draft", verbose_name="Status"
    )
    published_at = models.DateTimeField(blank=True, null=True, verbose_name="Published At")
    featured = models.BooleanField(default=False, verbose_name="Featured Article")

    class Meta(BaseModel.Meta):
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ==========================
# Breaking News
# ==========================
class BreakingNews(BaseModel):
    headline = models.CharField(max_length=255, verbose_name="Headline")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    content = RichTextUploadingField(verbose_name="Content")
    url = models.URLField(blank=True, null=True, verbose_name="URL")
    image = models.ImageField(
        upload_to="breaking_news/", blank=True, null=True, verbose_name="Breaking News Image"
    )
    active = models.BooleanField(default=True, verbose_name="Active")

    class Meta(BaseModel.Meta):
        verbose_name = "Breaking News"
        verbose_name_plural = "Breaking News"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.headline)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.headline


# ==========================
# Comment
# ==========================
class Comment(BaseModel):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Article",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="User",
    )
    content = RichTextUploadingField(verbose_name="Content")
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="replies",
        on_delete=models.CASCADE,
        verbose_name="Parent Comment",
    )

    class Meta(BaseModel.Meta):
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.user} on {self.article}"

    @property
    def is_reply(self):
        return self.parent is not None
