from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from better_profanity import profanity


# Create your models here.
class PostManager(models.Manager):
    def published_posts(self):
        return super().get_queryset().filter(status="P").order_by("-publish")


class Post(models.Model):
    STATUS_CHOICES = (
        ("D", "Draft"),
        ("P", "Published"),
    )
    objects = PostManager()
    title = models.CharField("Post Title", max_length=100)
    slug = models.SlugField(unique=True, blank=False, null=False)
    author = models.CharField("Auther name", max_length=30)
    body = models.TextField("Post body", max_length=2000)
    publish = models.DateTimeField("Data of publish", default=timezone.now)
    created = models.DateTimeField("Data of create", default=timezone.now)
    updated = models.DateTimeField("Data of last update", default=timezone.now)
    status = models.CharField(default="P",
                              max_length=10,
                              choices=STATUS_CHOICES)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        self.uniquify()

        super().save(*args, **kwargs)

    def uniquify(self):
        if Post.objects.filter(slug=self.slug).exists():
            slug = self.slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{slug}-{counter}"
                counter += 1


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_name = models.CharField("Author Name", max_length=50)
    email = models.EmailField("Author Email", max_length=256)
    body = models.TextField("Comment Body", max_length=500)
    created = models.DateTimeField("Data of create", default=timezone.now)
    updated = models.DateTimeField("Data of last update", default=timezone.now)
    isActive = models.BooleanField("is active", default=True)

    def save(self, *args, **kwargs):
        self.body = profanity.censor(self.body)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.body
