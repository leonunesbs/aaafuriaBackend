from django.urls import path, include
from .views import (
    login,
    cadastro,
    reauthenticate,
    is_authenticated,
    is_staff,
    pedidos_user,
    pedidos_admin,
    financeiro,
    financeiro_last_in,
    financeiro_last_out,
    financeiro_entries,
)

app_name = 'core'
urlpatterns = [
    path('login/', login),
    path('is-authenticated/', is_authenticated),
    path('is-staff/', is_staff),
    path('cadastro/', cadastro),
    path('token-login/', reauthenticate),
    path('meus-pedidos/', pedidos_user),
    path('pedidos-admin/', pedidos_admin),
    path('financeiro/', financeiro),
    path('financeiro-last-in/', financeiro_last_in),
    path('financeiro-last-out/', financeiro_last_out),
    path('financeiro-entries/', financeiro_entries),
]
