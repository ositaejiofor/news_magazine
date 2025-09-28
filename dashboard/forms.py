from django import forms
from news.models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'slug', 'category', 'tags', 'author', 'content', 'featured_image', 'status']
