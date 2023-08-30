import datetime

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from better_profanity import profanity


# Create your models here.
class PublishedPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="P").order_by("-publish")


class AllPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("-publish")


class Post(models.Model):
    STATUS_CHOICES = (
        ("D", "Draft"),
        ("P", "Published"),
    )
    published_ojects = PublishedPostManager()
    all_objects = AllPostManager()
    title = models.CharField("Post Title", max_length=100)
    slug = models.SlugField(unique=True, blank=False, null=False)
    author = models.CharField("Auther name", max_length=30)
    body = models.TextField("Post body", max_length=2000)
    publish = models.DateTimeField("Data of publish", default=timezone.now)
    created = models.DateTimeField("Data of create", auto_now_add=True)
    updated = models.DateTimeField("Data of last update", auto_now=True)
    status = models.CharField(default="P",
                              max_length=10,
                              choices=STATUS_CHOICES)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        self.uniquify()

        self.body = profanity.censor(self.body)

        super().save(*args, **kwargs)

    def uniquify(self):
        if Post.all_objects.filter(slug=self.slug).exists():
            last_char = self.slug[-1]
            if last_char.isdigit():
                num = int(last_char)
                if num == 9:
                    self.slug = self.slug[:-1] + "10"
                else:
                    self.slug = self.slug[:-1] + str(num + 1)
            else:
                self.slug += "-1"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_name = models.CharField("Author Name", max_length=50)
    email = models.EmailField("Author Email", max_length=256)
    body = models.TextField("Comment Body", max_length=500)
    created = models.DateTimeField("Data of create", auto_now_add=True)
    updated = models.DateTimeField("Data of last update", auto_now=True)
    isActive = models.BooleanField("is active", default=True)

    def is_there_comment_in_recent_30_sec(self):
        try:
            Comment.objects.get(email=self.email, updated__gte=timezone.now() - datetime.timedelta(seconds=30))
            return True
        except Comment.DoesNotExist:
            return False

    def save(self, *args, **kwargs):
        if self.is_there_comment_in_recent_30_sec():
            raise Exception("You can't comment twice in 30 seconds.")

        self.body = profanity.censor(self.body)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.body
