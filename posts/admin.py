from django.contrib import admin

from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publish", "status")

    def add_view(self, request, form_url="", extra_context=None):
        self.exclude = ("slug", "created", "updated")
        return super().add_view(request)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        self.exclude = ()
        return super().change_view(request, object_id)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "post", "body", "updated", "isActive")

    def add_view(self, request, form_url="", extra_context=None):
        self.exclude = ("created", "updated", "isActive")
        return super().add_view(request)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        self.exclude = ()
        return super().change_view(request, object_id)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
