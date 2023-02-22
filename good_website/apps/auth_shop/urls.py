from django.urls import path

from .views import *

app_name = "auth_shop"

urlpatterns = [
  path('', Login.as_view(), name="auth_shop"),
  path('create/', CreateUserView.as_view(), name="create"),
]
