from rest_framework import viewsets
import django_filters
from django_filters import rest_framework as filters
from inspection.models import Matter
from .serializers import MatterSerializer


class MatterFilter(filters.Filter):
    """Complaint Sheet 案件用フィルタクラス"""

    sales_person__contains = filters.CharFilter(field_name='sales_person', lookup_expr='icontains')
    customer__contains = filters.CharFilter(field_name='customer__customer_name', lookup_expr='icontains')

    class Meta:
        model = Matter
        fields = '__all__'


class MatterViewSet(viewsets.ModelViewSet):
    """Complaint Sheet 案件CRUD用のAPIクラス"""

    queryset = Matter.objects.all()
    queryset = queryset.order_by('-created_at')
    serializer_class = MatterSerializer
