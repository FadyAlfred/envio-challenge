from datetime import datetime

from django.utils import timezone
from rest_framework import serializers

from core.models import Reading
from core.utils import DateTimeFieldWithOffset


class ReadingSerializer(serializers.ModelSerializer):
    timestamp = DateTimeFieldWithOffset()
    device_id = serializers.UUIDField(source='device')
    customer_id = serializers.UUIDField(source='customer')

    class Meta:
        model = Reading
        fields = ('timestamp', 'device_id', 'customer_id', 'value')


class ReadingValueAggregatedSerializer(serializers.Serializer):
    reading_from_date = DateTimeFieldWithOffset(source='from')
    value = serializers.FloatField()


class ReadingAggregatedSerializer(serializers.Serializer):
    device_id = serializers.IntegerField(source='device')
    customer_id = serializers.IntegerField(source='customer')
    from_date = DateTimeFieldWithOffset(source='from')
    to_date = DateTimeFieldWithOffset(source='to')
    aggregation_size_minutes = serializers.IntegerField()
    aggregated_values = ReadingValueAggregatedSerializer(many=True)

    @staticmethod
    def serialize_aggregated_data(aggregated_date, time_interval, start_date, end_date):
        devices_map = {}
        devices_owner = {}
        for record in aggregated_date:
            device_id = record.get('device_id')
            aggregated_reading = {
                "from": record.get("timestamp").isoformat(),
                "value": record.get("value_avg")
            }
            if device_id in devices_map:
                devices_map[device_id].append(aggregated_reading)
            else:
                devices_map[device_id] = [aggregated_reading]

            if record.get(device_id) not in devices_owner:
                devices_owner[device_id] = record.get('customer_id')

        end_date = end_date if end_date else datetime.now(timezone.utc).isoformat()
        result = []

        for device in devices_map:
            obj = {
                "device_id": device,
                "customer_id": devices_owner.get(device),
                "from": start_date,
                "to": end_date,
                "aggregation_size_minutes": time_interval,
                "aggregated_values": devices_map.get(device)
            }
            result.append(obj)

        return result
