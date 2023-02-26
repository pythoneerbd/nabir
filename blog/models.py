from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from accounts.models import Accounts
#For youtube video show
from embed_video.fields import EmbedVideoField
# Create your models here.

class Category(MPTTModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True,verbose_name='Adres SEO')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class PublishedManager(models.Manager):
    def get_queryset(self):
       '''select only published posts'''
       return super(PublishedManager, self).get_queryset().filter(status="published")


class Post(models.Model):
    author = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    body = RichTextUploadingField()
    image = models.FileField(upload_to='photos/%Y/%m/%d')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    posted = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager()  # the default manager
    published_objects = PublishedManager()  # The publish-specific manager.
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:single_article', args=[self.id])

    def get_previous_post(self):
        try:
            return self.get_previous_by_posted()
        except Post.DoesNotExist:
            return None

    def get_next_post(self):
        try:
            return self.get_next_by_posted()
        except Post.DoesNotExist:
            return None

    class Meta:
        ordering = ['-posted', ]

    def __str__(self):
        return self.title


class Comment(MPTTModel):

    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    email = models.EmailField()
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['publish']

    def __str__(self):
        return self.name

class VideoPost(models.Model):
    title = models.CharField(max_length=100)
    video = EmbedVideoField()
    posted = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-posted', ]
