from django.db import models

# Create your models here.
class NewsLetterUsers(models.Model):
    """Email for subscribing confirmation"""
    email = models.EmailField(unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'NewsLetter Users'

    def __str__(self):
        return self.email