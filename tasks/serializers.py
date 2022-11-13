from rest_framework import serializers
from .models import Category, Task


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color']
        read_only_fields = ['created_by']


class TaskReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'is_completed', 'created_at', 'updated_at']

class TaskWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'is_completed']
               
    
class TaskCompletionStatSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()
    class Meta:
        model = Task
        fields = ['is_completed', 'count']
        
