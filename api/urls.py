from django.urls import path, include
from rest_framework.authtoken import views
from . views import (
    login, 
    cadastro,
    reauthenticate, 
    product_list, 
    product_detail, 
    remove_from_cart,
    add_to_cart, 
    get_carrinho_total, 
    carrinho,
    checkout,
    is_authenticated,
    is_staff,
    create_payment,
    pedidos_user,
    pedidos_admin
    
    )
 
app_name = 'api'
urlpatterns = [
    path('login/', login),
    path('is-authenticated/', is_authenticated),
    path('is-staff/', is_staff),
    path('cadastro/', cadastro),
    path('token-login/', reauthenticate),
    path('product-list/', product_list),
    path('product-detail/<int:pk>/', product_detail),
    path('carrinho/', carrinho),
    path('meus-pedidos/', pedidos_user),
    path('pedidos-admin/', pedidos_admin),
    path('add-to-cart/', add_to_cart),
    path('remove-from-cart/', remove_from_cart),
    path('get-carrinho-total/', get_carrinho_total),
    path('checkout/', checkout),
    path('create-payment/', create_payment),
]
