from rest_framework import viewsets
from .serializers import CategorySerializer
from .models import Category

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()