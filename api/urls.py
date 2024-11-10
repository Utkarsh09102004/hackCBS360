# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('process-string/', BasicResponseView.as_view(), name='process-string'),
    # path('order/<int:order_id>/', OrderDetail.as_view(), name='order-detail'),
]
