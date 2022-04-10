from django.urls import path

from .views import ProductListView, ProductView


urlpatterns = [
    path('<int:shop_id>/categories/<int:category_id>/', ProductListView.as_view()),
    path('<int:shop_id>/categories/<int:category_id>/<int:pk>/', ProductView.as_view()),
]
