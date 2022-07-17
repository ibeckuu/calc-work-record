import django_filters
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from inspection.models import Item, District, Customer, OrderStatus, InspectSchedule, InspectRecord, WorkingRecord, \
    OtherEvents, Operator
from .serializers import ItemSerializer, DistrictSerializer, CustomerSerializer, OrderStatusSerializer
from .serializers import InspectScheduleSerializer, InspectRecordSerializer, WorkingRecordSerializer, \
    OtherEventsSerializer, OperatorListSerializer, InspectSerializer


class ItemFilter(filters.FilterSet):
    """アイテムモデルのフィルタクラス"""

    description__contains = filters.CharFilter(field_name='description', lookup_expr='icontains')
    id__exact = filters.Filter(field_name='id', lookup_expr='exact')

    class Meta:
        model = Item
        exclude = ['inspected_qty']


class ItemViewSet(viewsets.ModelViewSet):
    """アイテムリストモデルのCRUD用APIクラス"""

    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ItemFilter
    # permission_classes = [IsAdminUser]


class DistrictFilter(filters.FilterSet):
    """地区モデルのフィルタクラス"""

    delete__exact = filters.Filter(field_name='is_delete', lookup_expr='exact')

    class Meta:
        model = District
        fields = '__all__'


class DistrictViewSet(viewsets.ModelViewSet):
    """地区モデルのCRUD用APIクラス"""

    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [IsAdminUser]


class CustomerFilter(filters.FilterSet):
    """ユーザーモデル用フィルタクラス"""

    name__contains = filters.CharFilter(field_name='customer_name', lookup_expr='icontains')
    delete__exact = filters.Filter(field_name='is_delete', lookup_expr='exact')

    class Meta:
        model = Customer
        exclude = ['district']


class CustomerViewSet(viewsets.ModelViewSet):
    """ユーザーモデルのCRUD用APIクラス"""

    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CustomerFilter
    # permission_classes = [IsAdminUser]


class OrderStatusFilterSet(filters.FilterSet):
    """オーダー履歴用フィルタクラス"""

    date__exact = filters.DateFilter(field_name='scheduled_shipping_date', lookup_expr='exact')
    producerid__exact = filters.Filter(field_name='item__producer_id', lookup_expr='exact')

    class Meta:
        model = OrderStatus
        fields = '__all__'


class OrderStatusViewSet(viewsets.ModelViewSet):
    """オーダー履歴のCRUD用APIクラス"""

    queryset = OrderStatus.objects.all()
    queryset = queryset.order_by('scheduled_shipping_date')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = OrderStatusFilterSet
    serializer_class = OrderStatusSerializer
    permission_classes = [IsAuthenticated]


class InspectScheduleFilterSet(filters.FilterSet):
    """検査スケジュール用フィルタクラス"""

    operator_id = filters.Filter(field_name='operator_id', lookup_expr='exact')
    latest__gte = filters.DateFilter(field_name='scheduled_inspect_date', lookup_expr='gte')
    date__exact = filters.DateFilter(field_name='scheduled_inspect_date', lookup_expr='exact')
    producerid__exact = filters.Filter(field_name='item__producer_id', lookup_expr='exact')

    class Meta:
        model = InspectSchedule
        exclude = ['created_at']


class InspectScheduleViewSet(viewsets.ModelViewSet):
    """検査スケジュールのCRUD用APIクラス"""

    queryset = InspectSchedule.objects.all()
    queryset = queryset.order_by('scheduled_inspect_date')
    serializer_class = InspectScheduleSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = InspectScheduleFilterSet
    permission_classes = [IsAuthenticated]


class InspectRecordViewSet(viewsets.ModelViewSet):
    """検査実績のCRUD用APIクラス"""

    queryset = InspectRecord.objects.all()
    serializer_class = InspectRecordSerializer
    permission_classes = [IsAdminUser]


class InspectFilter(filters.FilterSet):
    """DisplayInspectRecord用フィルタクラス"""

    qualified__gt = filters.NumberFilter(field_name='inspect_qty', lookup_expr='gt')
    operator_id = filters.Filter(field_name='operator_id', lookup_expr='exact')
    latest__gte = filters.DateFilter(field_name='inspect_date', lookup_expr='gte')
    date__exact = filters.DateFilter(field_name='inspect_date', lookup_expr='exact')
    date__gte = filters.DateFilter(field_name='inspect_date', lookup_expr='gte')
    date__lt = filters.DateFilter(field_name='inspect_date', lookup_expr='lt')
    inspect__gt = filters.NumberFilter(field_name='inspect_qty', lookup_expr='gt')
    shipping__gt = filters.NumberFilter(field_name='shipping_qty', lookup_expr='gt')

    class Meta:
        model = InspectRecord
        fields = '__all__'


class InspectViewSet(viewsets.ModelViewSet):
    """検査実績一覧表示用のAPIクラス"""

    serializer_class = InspectSerializer
    queryset = InspectRecord.objects.all()
    queryset = queryset.order_by('inspect_date', 'created_at')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = InspectFilter


class InspectMonthlyViewSet(viewsets.ModelViewSet):
    """検査実績一覧表示用のAPIクラス"""

    serializer_class = InspectSerializer
    queryset = InspectRecord.objects.all()
    queryset = queryset.order_by('created_at')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = InspectFilter


# class AggregateInspectThisMonthViewSet(viewsets.ModelViewSet):
    """当月検査実績集計APIクラス"""

    # serializer_class = AggregateThisMonthWorkingSerializer
    # queryset = serializer_class.data
    # queryset = queryset.order_by('created_at')
    # filter_backends = [filters.DjangoFilterBackend]
    # filterset_class = InspectFilter

    # def list(self, request, *args, **kwargs):
    #     queryset = WorkingRecord.objects.raw("SELECT * from working_record where working_date > '2022-01-01';")
        # serializer = WorkingRecordSerializer(queryset, many=True)
        # return Response(serializer.data)


class InspectQualifiedViewSet(viewsets.ModelViewSet):
    """検査実績表示用のAPIクラス"""

    serializer_class = InspectRecordSerializer
    queryset = InspectRecord.objects.all()
    queryset = queryset.order_by('-created_at')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = InspectFilter


class ShippingFilter(filters.FilterSet):
    """ShippingRecord用フィルタクラス"""

    date__gte = filters.DateFilter(field_name='inspect_date', lookup_expr='gte')
    date__lt = filters.DateFilter(field_name='inspect_date', lookup_expr='lt')
    shipping__gt = filters.NumberFilter(field_name='shipping_qty', lookup_expr='gt')

    class Meta:
        model = InspectRecord
        fields = '__all__'


class ShippingYearlyViewSet(viewsets.ModelViewSet):

    serializer_class = InspectSerializer
    queryset = InspectRecord.objects.all()
    queryset = queryset.order_by('inspect_date', 'created_at')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ShippingFilter


class WorkingRecordFilter(filters.FilterSet):
    """作業履歴用フィルタクラス"""

    operator_id = filters.Filter(field_name='operator_id', lookup_expr='exact')
    latest__gte = filters.DateFilter(field_name='working_date', lookup_expr='gte')
    date__exact = filters.DateFilter(field_name='working_date', lookup_expr='exact')
    working_minutes__gt = filters.Filter(field_name='working_minutes', lookup_expr='gt')
    date__gte = filters.DateFilter(field_name='working_date', lookup_expr='gte')
    date__lt = filters.DateFilter(field_name='working_date', lookup_expr='lt')

    class Meta:
        model = WorkingRecord
        fields = '__all__'


class WorkingRecordViewSet(viewsets.ModelViewSet):
    """作業履歴のCRUD用APIクラス"""

    queryset = WorkingRecord.objects.all()
    queryset = queryset.order_by('working_date', 'created_at')
    serializer_class = WorkingRecordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = WorkingRecordFilter


class OtherEventsFilter(filters.FilterSet):
    """イベント用フィルタクラス"""

    latest__gte = filters.DateFilter(field_name='event_date', lookup_expr='gte')
    date__exact = filters.DateFilter(field_name='event_date', lookup_expr='exact')

    class Meta:
        model = OtherEvents
        fields = '__all__'


class OtherEventsViewSet(viewsets.ModelViewSet):
    """その他イベントのCRUD用APIクラス"""

    queryset = OtherEvents.objects.all()
    serializer_class = OtherEventsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = OtherEventsFilter


class OperatorFilter(filters.FilterSet):
    """担当者モデル用のフィルタクラス"""

    working__exact = filters.BooleanFilter(field_name='is_working', lookup_expr='exact')

    class Meta:
        model = Operator
        fields = '__all__'


class OperatorViewSet(viewsets.ModelViewSet):
    """担当者モデルのCRUD用APIクラス"""

    serializer_class = OperatorListSerializer
    queryset = Operator.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = OperatorFilter
