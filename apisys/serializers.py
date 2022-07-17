from rest_framework import serializers
from inspection.models import Matter


class MatterSerializer(serializers.ModelSerializer):

    customer_name = serializers.ReadOnlyField(source='customer.customer_name')

    class Meta:
        model = Matter
        fields = '__all__'
