from django.urls import path
from api.views import JsonRpcView

urlpatterns = [
    path("jsonrpc/", JsonRpcView.as_view(), name="jsonrpc"),
]
