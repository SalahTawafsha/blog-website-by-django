from rest_framework.permissions import IsAuthenticated, BasePermission


class AuthenticatedPostPermission(IsAuthenticated):
    allowed_methods = ['GET', 'POST', 'PUT', 'DELETE']

    def has_permission(self, request, view):
        # Check if the request method is in the allowed_methods list
        if request.method in self.allowed_methods:
            return super().has_permission(request, view)
        return False


class AnonymousPostPermission(BasePermission):
    def has_permission(self, request, view):
        # Check if the request method is in the allowed_methods list
        if request.method == "GET":
            return True  # Allow anonymous access for specified methods
        return False


class UserPermission(IsAuthenticated):
    allowed_methods = ['GET', 'POST']

    def has_permission(self, request, view):
        # Check if the request method is in the allowed_methods list
        if request.method in self.allowed_methods:
            return super().has_permission(request, view)
        return False


class CommentPermission(BasePermission):
    allowed_methods = ['GET', 'POST']  # Add the HTTP methods you want to allow for anonymous users

    def has_permission(self, request, view):
        # Check if the request method is in the allowed_methods list
        if request.method in self.allowed_methods:
            return super().has_permission(request, view)
        return False
