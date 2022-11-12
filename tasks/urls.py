from rest_framework import routers
from .views import CategoryViewSet, TaskViewSet

router = routers.DefaultRouter()
router.register('api/categories', CategoryViewSet, 'categories')
router.register('api/tasks', TaskViewSet, 'tasks')

urlpatterns = router.urls
