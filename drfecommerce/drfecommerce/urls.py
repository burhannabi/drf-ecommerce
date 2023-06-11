from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from drfecommerce.product import views

router = routers.DefaultRouter()
router.register(r"category", views.CategoryViewSet)
router.register(r"product", views.ProductViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="schema_docs",
    ),
]
