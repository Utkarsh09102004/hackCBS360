# myproject/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# from products.views import ProductViewSet  # Import the viewset for your products

# Set up the schema view for Swagger UI
schema_view = get_schema_view(
    openapi.Info(
        title="Order API",
        default_version="v1",
        description="API for managing products",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Set up the router and register your viewsets
router = DefaultRouter()
router.register(r'products', ProductViewSet)  # Register your product viewset

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Include the app's API paths
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),  # Swagger JSON schema
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),  # Swagger UI page
]