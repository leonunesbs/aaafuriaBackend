from django.urls import path, include
from .views import *

app_name = 'core'
urlpatterns = [
    path('authentication/', AuthenticationView.as_view()),
    path('seja-socio/', SejaSócioView.as_view()),
    path('cadastro/', cadastro),
    path('token-login/', reauthenticate),
    path('pedidos-user/', pedidos_user),
    path('pedidos-admin/', pedidos_admin),
    path('status-pedido-admin/', status_pedido_admin),
    path('financeiro/', financeiro),
    path('financeiro-last-in/', financeiro_last_in),
    path('financeiro-last-out/', financeiro_last_out),
    path('financeiro-entries/', financeiro_entries),
    path('associacao/', AssociaçãoView.as_view()),
    path('get-admin-associacao/', get_admin_associação),
    path('toggle-associacao/<int:pk>/', toggle_associação),
]
