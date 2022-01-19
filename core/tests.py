import uuid
from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Reading, Customer, Device


class TestReadingView(APITestCase):
    def setUp(self):
        self.url = reverse('reading')

    def test_send_request_success(self):
        """
        In this method we test add new reading successfully.
        """

        body = {
            "timestamp": "2017-01-15T12:18:49.541124+00:00",
            "device_id": str(uuid.uuid4()),
            "customer_id": str(uuid.uuid4()),
            "value": 12.6
        }
        response = self.client.post(self.url, body)

        readings_count = Reading.objects.count()
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(readings_count, 1)


class TestReadingAggregateView(APITestCase):
    def setUp(self):
        self.url = reverse('reading-aggregator')
        self.customer = Customer.objects.create()
        self.device = Device.objects.create(customer=self.customer)
        timestamp = datetime.now()
        values = [540, 600, 350]

        for value in values:
            Reading.objects.create(timestamp=timestamp, value=value, customer=self.customer, device=self.device)

        self.avg_value = round(sum(values) / len(values), 2)

    def test_send_request_success(self):
        """
        In this method we test retrieve aggregated reading successfully.
        """
        response = self.client.get(self.url)
        data = response.json()
        reading_aggregated_object = data[0]

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(reading_aggregated_object.get('device_id'), str(self.device.id))
        self.assertEqual(reading_aggregated_object.get('customer_id'), str(self.customer.id))
        self.assertEqual(reading_aggregated_object.get('aggregated_values')[0].get('value'), self.avg_value)
