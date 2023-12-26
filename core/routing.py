from Transactions.consumers import TransactionsConsumer1
from Payments.consumers import PaymentsConsumer1
from Metrics.consumers import MetricsConsumer1
from core.consumers import FallbackConsumer
from Swaps.consumers import SwapsConsumer1
from Pools.consumers import PoolsConsumer1
from django.urls import path


websocket_urlpatterns = [
    path('ws/transactions1/<slug:uidb64>/', TransactionsConsumer1.as_asgi()),
    path('ws/payments1/', PaymentsConsumer1.as_asgi()),
    path('ws/metrics1/<slug:uidb64>/', MetricsConsumer1.as_asgi()),
    path('ws/swaps1/<slug:uidb64>/', SwapsConsumer1.as_asgi()),
    path('ws/pools1/<slug:uidb64>/', PoolsConsumer1.as_asgi()),
    path('ws/', FallbackConsumer.as_asgi()),

]

