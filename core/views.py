from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import Customer, Device, Reading
from core.serializers import ReadingSerializer, ReadingAggregatedSerializer


class ReadingView(APIView):

    @swagger_auto_schema(request_body=ReadingSerializer)
    def post(self, request):
        serializer = ReadingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        # Create customer and device if not exist and check if the device owned by another customer
        customer, _ = Customer.objects.get_or_create(id=data.get('customer_id'))
        try:
            device = Device.objects.get(id=data.get('device_id'))
            if device.customer != customer:
                return Response({"message": "Device already associated with another customer"},
                                status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            device = Device.objects.create(id=data.get('device_id'), customer=customer)
        Reading.objects.create(
            timestamp=data.get('timestamp'), value=data.get('value'), customer=customer, device=device
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReadingAggregateView(APIView):
    @swagger_auto_schema(responses={200: ReadingAggregatedSerializer},
                         manual_parameters=[
                             openapi.Parameter('from', openapi.IN_QUERY, type=openapi.TYPE_STRING),
                             openapi.Parameter('to', openapi.IN_QUERY, type=openapi.TYPE_STRING),
                             openapi.Parameter('customer_id', openapi.IN_QUERY, type=openapi.TYPE_STRING),
                             openapi.Parameter('device_id', openapi.IN_QUERY, type=openapi.TYPE_STRING),
                             openapi.Parameter('interval', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
                         ])
    def get(self, request):
        # The query parameters user can use
        start_date = self.request.GET.get('from', None)
        end_date = self.request.GET.get('to', None)
        customer_id = self.request.GET.get('customer_id', None)
        device_id = self.request.GET.get('device_id', None)
        time_interval = self.request.GET.get('interval', 5)

        # Validate start_date and end_date and interval query params
        if start_date:
            try:
                start_date = datetime.fromisoformat(start_date)
            except ValueError as e:
                return Response({"message": "Query Parameter start date has wrong format"},
                                status=status.HTTP_400_BAD_REQUEST)
        if end_date:
            try:
                end_date = datetime.fromisoformat(end_date)
            except ValueError as e:
                return Response({"message": "Query Parameter end date has wrong format"},
                                status=status.HTTP_400_BAD_REQUEST)

        # To handle in case came with empty string
        if not time_interval:
            time_interval = 5

        records = Reading.objects.aggregate_readings(start_date, end_date, time_interval, customer_id, device_id)
        aggregated_data = ReadingAggregatedSerializer.serialize_aggregated_data(
            records, time_interval, start_date, end_date)

        return Response(aggregated_data, status=status.HTTP_200_OK)
