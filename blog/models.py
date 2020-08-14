import random
import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse

from taggit.managers import TaggableManager

from .helpers import upload_path, count_words, read_time

"""
Contains Models For The Blog:
1. PostCategory
2. Post
3. Comment

Above are the enlisting of the models in this files in order in
which they were written
"""

User = get_user_model()


#########################################################
#                 POST CATEGORY MODEL
#########################################################
class PostCategoryManager(models.Manager):
    def get_queryset(self):
        return super(PostCategoryManager, self).get_queryset().filter(
            approve=True
        )


class PostCategory(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    image = models.ImageField()
    approve = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('title',)
        verbose_name = 'post_category'
        ordering = ('-updated', )

    objects = models.Manager()
    approved = PostCategoryManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.title} - {uuid.uuid4()} - {random.randint(1, 9999999999)}", allow_unicode=True)
        super(PostCategory, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})


#########################################################
#                 POST MODEL
#########################################################
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
            .filter(active=True, status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250, unique_for_date='published_date'
    )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    # category = models.ForeignKey(PostCategory, on_delete=models.CASCADE, related_name="posts")
    tags = TaggableManager()
    body = models.TextField()
    image = models.ImageField(upload_to=upload_path)
    views = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    words_count = models.PositiveIntegerField(default=0)
    read_duration = models.CharField(max_length=50, default=0)
    published_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft'
                              )

    class Meta:
        ordering = ('-published_date', )

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.status

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.title} - {random.randint(1, 9999999999)} - {uuid.uuid4()}")
        self.words_count = count_words(self.body)
        self.read_duration = read_time(self.body)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.published_date.year,
                                                 self.published_date.month,
                                                 self.published_date.day, self.slug])

    def get_delete_url(self):
        return reverse('blog:post_delete', args=[self.published_date.year,
                                                 self.published_date.month,
                                                 self.published_date.day, self.slug])


#########################################################
#                 POST COMMENT MODEL
#########################################################
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # name = models.CharField(max_length=80)
    # email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
