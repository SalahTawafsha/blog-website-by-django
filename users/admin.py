from django.contrib import admin

from users.models import UserTracking


# Register your models here.
@admin.register(UserTracking)
class UserTrackingAdmin(admin.ModelAdmin):
    list_display = (
        "user", "warnings_num", "day_read_posts_num", "day_create_posts_num", "date_of_start_block",
        "date_of_end_block", "allowed_read_post_date")
