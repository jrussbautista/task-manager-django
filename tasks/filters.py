from django_filters.rest_framework import FilterSet
from .models import Task


class TaskFilter(FilterSet):
    class Meta:
        model = Task
        fields = {"category_id": ["exact"], "is_completed": ["exact", "in"]}
