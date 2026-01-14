from django.db import models
from django.contrib.auth.models import User

class AIPost(models.Model):
    # link post to user so they can only see their own posts
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # What the user asked for
    topic = models.CharField(max_length=200)
    tone = models.CharField(max_length=50)

    # What the AI generated
    generated_content = models.TextField()

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.topic} - {self.created_at.strftime('%Y-%m-%d')}"
