
from rest_framework import serializers
from inspection.models import Item, District, Customer, OrderStatus, InspectSchedule, InspectRecord, WorkingRecord, \
    OtherEvents, Operator
import re


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class OrderStatusSerializer(serializers.ModelSerializer):

    start = serializers.ReadOnlyField(source='scheduled_shipping_date')
    title = serializers.SerializerMethodField()
    item_description = serializers.ReadOnlyField(source='item.description')
    item_inspected_qty = serializers.ReadOnlyField(source='item.inspected_qty')
    customer_name = serializers.ReadOnlyField(source='customer.customer_name')
    producer_id = serializers.ReadOnlyField(source='item.producer_id')

    def get_title(self, obj):
        return '{} / {}個'.format(obj.item.short_name, obj.order_qty)

    class Meta:
        model = OrderStatus
        fields = '__all__'


class InspectScheduleSerializer(serializers.ModelSerializer):

    start = serializers.ReadOnlyField(source='scheduled_inspect_date')
    title = serializers.SerializerMethodField()
    item_description = serializers.ReadOnlyField(source='item.description')
    operator_name = serializers.ReadOnlyField(source='operator.operator_name')
    producer_id = serializers.ReadOnlyField(source='item.producer_id')

    def get_title(self, obj):
        return '{} / {}'.format(obj.item.short_name, obj.operator)

    class Meta:
        model = InspectSchedule
        fields = '__all__'


class InspectSerializer(serializers.ModelSerializer):

    item_description = serializers.ReadOnlyField(source='item.description')
    operator_name = serializers.ReadOnlyField(source='operator.operator_name')
    customer_name = serializers.ReadOnlyField(source='customer.customer_name')
    customer_district_code = serializers.ReadOnlyField(source='customer.district.district_code')
    producer_id = serializers.ReadOnlyField(source='item.producer_id')
    ordinary_description = serializers.SerializerMethodField()
    ordinary_item_number = serializers.SerializerMethodField()

    class Meta:
        model = InspectRecord
        fields = '__all__'

    def get_ordinary_description(self, obj):
        if obj.item.description is not None:
            return re.sub(r'(-R$|-B8$)', '', obj.item.description)
        return None

    def get_ordinary_item_number(self, obj):
        if obj.item.id is not None:
            return obj.item.id % 10000000
        return None


class InspectRecordSerializer(serializers.ModelSerializer):

    start = serializers.ReadOnlyField(source='inspect_date')
    title = serializers.SerializerMethodField()
    qualified_qty = serializers.SerializerMethodField()

    def get_title(self, obj):
        return '{}, {}個, {}'.format(obj.item.short_name, obj.inspect_qty - obj.defective_qty, obj.operator)

    def get_qualified_qty(self, obj):
        return obj.inspect_qty - obj.defective_qty

    class Meta:
        model = InspectRecord
        fields = '__all__'


class WorkingRecordSerializer(serializers.ModelSerializer):

    operator_name = serializers.ReadOnlyField(source='operator.operator_name')
    customer_name = serializers.ReadOnlyField(source='customer.customer_name')
    customer_district = serializers.ReadOnlyField(source='customer.district.district_code')

    class Meta:
        model = WorkingRecord
        fields = '__all__'


class OtherEventsSerializer(serializers.ModelSerializer):

    start = serializers.ReadOnlyField(source='event_date')
    title = serializers.ReadOnlyField(source='event_title')

    class Meta:
        model = OtherEvents
        fields = '__all__'


class OperatorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Operator
        fields = '__all__'
