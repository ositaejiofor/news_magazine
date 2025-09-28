from django.db import models
from django.contrib.auth.models import User
from news.models import Article
from news.models import Comment


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments_dashboard')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_user')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.article}'
