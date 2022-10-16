# To integrate the Django Project with Swagger Documentation

from email.policy import default
from rest_framework import permissions
from drf_yasg2 import openapi
from drf_yasg2.views import get_schema_view


# Swagger API view
schema_view = get_schema_view(
    openapi.Info(
        title="Rest Swagger", default_version="v1", description="Test Description"
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
