from django.urls import path, include
from .views import (
    login,
    logout,
    seja_sócio,
    cadastro,
    reauthenticate,
    is_authenticated,
    is_staff,
    pedidos_user,
    pedidos_admin,
    status_pedido_admin,
    financeiro,
    financeiro_last_in,
    financeiro_last_out,
    financeiro_entries,

    create_associação,
    get_user_associação,
    get_associação_category,
    get_admin_associação,
    toggle_associação
)

app_name = 'core'
urlpatterns = [
    path('login/', login),
    path('logout/', logout),
    path('seja-socio/', seja_sócio),
    path('is-authenticated/', is_authenticated),
    path('is-staff/', is_staff),
    path('cadastro/', cadastro),
    path('token-login/', reauthenticate),
    path('pedidos-user/', pedidos_user),
    path('pedidos-admin/', pedidos_admin),
    path('status-pedido-admin/', status_pedido_admin),
    path('financeiro/', financeiro),
    path('financeiro-last-in/', financeiro_last_in),
    path('financeiro-last-out/', financeiro_last_out),
    path('financeiro-entries/', financeiro_entries),
    path('create-associacao/', create_associação),
    path('get-user-associacao/', get_user_associação),
    path('get-associacao-category/<categoria>/', get_associação_category),
    path('get-admin-associacao/', get_admin_associação),
    path('toggle-associacao/<int:pk>/', toggle_associação),
]
