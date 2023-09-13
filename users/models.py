import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from posts.models import Post

# Create your models here.

NUMBER_OF_WARNINGS_TO_GET_BLOCK = 3
MAX_ALLOWED_READ_POSTS_IN_DAY = 3
MAX_ALLOWED_POST_POSTS_IN_DAY = 3


class UserTracking(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    warnings_num = models.SmallIntegerField("Number of Warnings",
                                            default=0)
    read_posts_num = models.SmallIntegerField("Number of Warnings",
                                              default=0)
    day_posts_num = models.SmallIntegerField("Number of created posts in a day",
                                             default=0)
    date_of_start_block = models.DateTimeField("date of start block", blank=True, null=True,
                                               default=None)
    date_of_end_block = models.DateTimeField("date of end block", blank=True, null=True,
                                             default=None)
    # date that user can read posts after it
    allowed_read_post_date = models.DateTimeField("date of last read post", blank=True, null=True,
                                                  default=timezone.now)

    read_posts = models.ManyToManyField(Post, related_name="read_user", )
    posts_likes = models.ManyToManyField(Post, related_name='users_liked')
    posts_dislikes = models.ManyToManyField(Post, related_name='users_disliked')
    subscriptions = models.ManyToManyField(User, related_name='subscribed_users')

    def increment_warnings(self, days_of_block=10):
        self.warnings_num = self.warnings_num + 1

        if self.warnings_num == NUMBER_OF_WARNINGS_TO_GET_BLOCK:
            self.date_of_start_block = timezone.now()
            self.date_of_end_block = (
                    self.date_of_start_block + datetime.timedelta(days=days_of_block))
            self.warnings_num = 0

        self.save()

    def like_post(self, post):
        self.posts_likes.add(post)

        if self.posts_dislikes.filter(id=post.id):
            self.posts_dislikes.remove(post)

        self.save()

    def dislike_post(self, post):
        self.posts_dislikes.add(post)

        if self.posts_likes.filter(id=post.id):
            self.posts_likes.remove(post)

        self.save()

    def subscribe(self, user):
        self.subscriptions.add(user)
        self.save()

    def is_blocked(self):
        if self.date_of_end_block:
            if self.date_of_end_block < timezone.now():
                self.date_of_start_block = None
                self.date_of_end_block = None
                self.save()
                return False
            else:
                return True
        else:
            return False

    def increment_read_posts(self, post):
        if post not in self.read_posts.all():
            self.read_posts.add(post)
            self.read_posts_num += 1
            if self.read_posts_num == MAX_ALLOWED_READ_POSTS_IN_DAY:
                self.allowed_read_post_date = timezone.now() + datetime.timedelta(days=1)
            self.save()

    def is_can_read_post(self):
        if self.allowed_read_post_date <= timezone.now():
            self.read_posts_num = 0
            self.allowed_read_post_date = timezone.now()
            return True
        else:
            return False

    def increment_num_of_created_posts(self):
        self.day_posts_num += 1
        self.save()

    def is_can_post_post(self):
        if self.day_posts_num == MAX_ALLOWED_POST_POSTS_IN_DAY:
            if (self.user.post_set.
                    filter(created__gte=timezone.now() - datetime.timedelta(days=1))):
                return False
            else:
                self.day_posts_num = 0
                return True
        else:
            return True


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserTracking.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.usertracking.save()
