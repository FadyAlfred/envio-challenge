from django.utils import timezone
from rest_framework import serializers


class DateTimeFieldWithOffset(serializers.DateTimeField):
    default_error_messages = {
        'naive': 'Datetime value is missing a timezone offset.'
    }

    def enforce_timezone(self, value):
        if timezone.is_naive(value):
            self.fail('naive')
        return super().enforce_timezone(value)


def dict_fetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
