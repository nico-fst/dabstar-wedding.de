from django.contrib import admin
from django.urls import path, include
from wedsite import views as wedsite_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("wedsite.urls"))
]
