from django.urls import path

from core.views import ReadingView, ReadingAggregateView

urlpatterns = [
    path('reading', ReadingView.as_view(), name='reading'),
    path('reading/aggregate', ReadingAggregateView.as_view(), name='reading-aggregator'),
]
