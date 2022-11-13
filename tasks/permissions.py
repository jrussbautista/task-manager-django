from rest_framework import permissions
from .models import Category

class TaskCategoryOwnPermission(permissions.BasePermission):
    message = 'Category not found'
    def has_permission(self, request, view):
        if view.action == 'create' or view.action == 'update' or view.action == 'partial_update':
            category = request.data.get('category')
            if category is None:
                return True
            ## check whether category is owned by user
            user_category_exists = Category.objects.filter(created_by=request.user, id=category).exists()
            return user_category_exists
        return True