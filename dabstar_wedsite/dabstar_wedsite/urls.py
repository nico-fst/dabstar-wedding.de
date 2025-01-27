from django.contrib import admin
from django.urls import path, include
from wedsite import views as wedsite_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("wedsite.urls"))
)