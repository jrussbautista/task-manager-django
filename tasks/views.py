
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CategorySerializer, TaskReadSerializer, TaskWriteSerializer, TaskCompletionStatSerializer
from .filters import TaskFilter
from .pagination import DefaultPagination
from .permissions import TaskCategoryOwnPermission
from .models import Task


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.categories.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, TaskCategoryOwnPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created_at', 'updated_at']
    ordering = ['created_at']

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return TaskWriteSerializer
        return TaskReadSerializer

    def get_queryset(self):
        return self.request.user.tasks.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        task = TaskReadSerializer(serializer.instance)
        return Response(task.data)


class TaskCompletionStatViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = self.request.user
        queryset = Task.objects.filter(created_by=user).values('is_completed').annotate(count=Count('is_completed'))
        serializer = TaskCompletionStatSerializer(queryset, many=True)
        return Response(serializer.data)