from django.urls import path, include
from .views import (
        product_list,
product_detail,
carrinho,
add_to_cart,
remove_from_cart,
get_carrinho_total,
checkout,
create_payment,
)

app_name = 'ecommerce'
urlpatterns = [
    path('product-list/', product_list),
    path('product-detail/<int:pk>/', product_detail),
    path('carrinho/', carrinho),
    path('add-to-cart/', add_to_cart),
    path('remove-from-cart/', remove_from_cart),
    path('get-carrinho-total/', get_carrinho_total),
    path('checkout/', checkout),
    path('create-payment/', create_payment),

]
