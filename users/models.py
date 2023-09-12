import datetime

import schedule
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from posts.models import Post

# Create your models here.

NUMBER_OF_WARNINGS_TO_GET_BLOCK = 3
DAYS_OF_BLOCK = 10
MAX_ALLOWED_READ_POSTS_IN_DAY = 3
MAX_ALLOWED_POST_POSTS_IN_DAY = 3


class UserTracking(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    warnings_num = models.SmallIntegerField("Number of Warnings",
                                            default=0)
    date_of_block = models.DateTimeField("date of blocked",
                                         default=None)
    read_posts_num = models.SmallIntegerField("Number of Warnings",
                                              default=0)
    day_posts_num = models.SmallIntegerField("Number of created posts in a day",
                                             default=0)

    read_posts = models.ManyToManyField(Post, related_name="read_user", )
    posts_likes = models.ManyToManyField(Post, related_name='users_liked')
    posts_dislikes = models.ManyToManyField(Post, related_name='users_disliked')
    subscriptions = models.ManyToManyField(User, related_name='subscribed_users')

    def increment_warnings(self):
        self.warnings_num = self.warnings_num + 1

        if self.warnings_num == NUMBER_OF_WARNINGS_TO_GET_BLOCK:
            self.date_of_block = timezone.now()
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
        if self.date_of_block:
            if self.date_of_block + datetime.timedelta(days=DAYS_OF_BLOCK) < timezone.now():
                self.date_of_block = None
                self.save()
                return False
            else:
                return True
        else:
            return False

    def increment_read_posts(self, post):
        if post not in self.read_posts.all():
            self.read_posts_num += 1
            self.read_posts.add(post)
            self.save()

    def is_can_read_post(self):
        if self.read_posts_num == MAX_ALLOWED_READ_POSTS_IN_DAY:
            return False
        else:
            return True

    def increment_post_posts(self):
        self.day_posts_num += 1
        self.save()

    def is_can_post_post(self):
        if self.day_posts_num == MAX_ALLOWED_POST_POSTS_IN_DAY:
            return False
        else:
            return True

    def reset(self):
        self.read_posts_num = 0
        self.day_posts_num = 0

    schedule.every().day.at("00:00").do(reset)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserTracking.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.usertracking.save()
