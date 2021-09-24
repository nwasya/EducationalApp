from django.urls import path

from Edu_book.views import ProductsList, product_detail, SearchProductsView

urlpatterns = [
    path('products', ProductsList.as_view(), name='products'),
    path('products/<productId>/<name>', product_detail, name='product_detail'),
    path('products/search', SearchProductsView.as_view()),

]
