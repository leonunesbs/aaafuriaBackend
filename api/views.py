import stripe
import json
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from rest_framework.decorators import (
    api_view,
    permission_classes
)

from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_200_OK
)


from rest_framework.response import Response


from ecommerce.models import Item, Order, OrderItem, ItemSize, Payment

from .serializers import ItemsSerializer, OrderItemSerializer, UserSerializer, OrderSerializer



@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username == '' or password == '' or username is None or password is None:
        return Response({'error': 'Por favor, forneça usuário e senha.'}, status=HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Credenciais inválidas'}, status=HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)

    user_serialized = UserSerializer(user)

    return Response({
        'token': token.key,
        'is_socio': user.sócio.is_sócio,
        'user': user_serialized.data
    }, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def is_authenticated(request):
    if request.user.sócio.is_sócio:
        return Response({'is_sócio': request.user.sócio.is_sócio}, status=HTTP_200_OK)
    return Response({'is_sócio': False},status=HTTP_200_OK)

@api_view(['POST'])
@permission_classes((AllowAny,))
def cadastro(request):
    min_len_pass = 6

    nome = request.data.get('nome')
    email = request.data.get('email')
    matricula = request.data.get('matricula')
    turma = request.data.get('turma')
    senha = request.data.get('senha')
    senha_again = request.data.get('senha_again')
    data_de_nascimento = request.data.get('data_de_nascimento')

    email = email.lower()

    if not (nome and email and matricula and turma and senha and senha_again and data_de_nascimento):
        return Response({'error': 'Todos os campos são obrigatórios'})

    if matricula and not matricula.isnumeric():
        return Response({'error': 'Sua matrícula deve conter apenas números'}, status=HTTP_400_BAD_REQUEST)

    if len(matricula) != 8:
        return Response({'error': 'Sua matrícula deve conter 8 dígitos'})

    if senha != senha_again:
        return Response({'error': 'As senhas não correspondem'}, status=HTTP_400_BAD_REQUEST)

    if len(senha) < min_len_pass:
        return Response({'error': f'Sua senha deve conter pelo menos {min_len_pass} dígitos'}, status=HTTP_400_BAD_REQUEST)

    if (int(turma) < 9 or int(turma) > 99):
        return Response({'error': 'Turma inválida'}, status=HTTP_400_BAD_REQUEST)
        
    try:
        user = User.objects.create_user(username=matricula, email=email, password=senha)
    except:
        return Response({'error': 'Sua matrícula já se encontra cadastrada'}, status=HTTP_409_CONFLICT)


    user.save()
    user.sócio.nome_completo = nome
    user.sócio.data_de_nascimento = data_de_nascimento
    user.sócio.save()

    token, _ = Token.objects.get_or_create(user=user)


    return Response({'token': token.key}, status=HTTP_200_OK)
    

@api_view(['POST'])
@permission_classes((AllowAny,))
def reauthenticate(request):
    tk = request.data.get('token')
    try:
        token = Token.objects.get(key=tk)
        return Response({'token': token.key}, status=HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'error': 'Credenciais inválidas'}, status=HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((AllowAny,))
def product_list(request):

    items = Item.objects.all()
    serializer = ItemsSerializer(items, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((AllowAny,))
def product_detail(request, pk):

    item = Item.objects.get(pk=pk)

    serializer = ItemsSerializer(item)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_to_cart(request):
        pk = request.data.get('pk')
        tamanho = request.data.get('tamanho')

        user = request.user
        order, order_created = Order.objects.get_or_create(user=user, ordered=False)

        item = Item.objects.get(pk=pk)


        if item.has_variations:
            item_variation = ItemSize.objects.get(item=item, size=tamanho)
            if item.has_stock and item_variation.stock == 0:
                return Response({'error': 'Tamanho fora de estoque', 'item': item.title}, status=HTTP_400_BAD_REQUEST)
            order_item, order_item_created = OrderItem.objects.get_or_create(
                user=user, 
                item=item,
                ordered=False,
                size=item_variation
            )
        else:
            if item.has_stock and item.stock == 0:
                return Response({'error': 'Item fora de estoque', 'item': item.title}, status=HTTP_400_BAD_REQUEST)
            order_item, order_item_created = OrderItem.objects.get_or_create(
                user=user, 
                item=item,
                ordered=False,
            )

        order.items.add(order_item)

        if not order_item_created:
            if item.has_stock:
                if item.has_variations:
                    if item_variation.stock >= (order_item.quantity + 1):
                        order_item.quantity += 1
                    else:
                        return Response({'error': 'Variação fora de estoque'}, status=HTTP_400_BAD_REQUEST)
                else:
                    if item.stock >= (order_item.quantity + 1):
                        order_item.quantity += 1
                    else:
                        return Response({'error': 'Item fora de estoque'}, status=HTTP_400_BAD_REQUEST)
            else:
                order_item.quantity += 1


        order.save()
        order_item.save()

        return Response({'message': 'Item adicionado ao Carrinho.'})

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def remove_from_cart(request):
    pk = request.data.get('pk')
    user = request.user
    try:
        order_item = OrderItem.objects.get(pk=pk, ordered=False)
        order_item.delete()
        return Response({'message': 'Item removido do Carrinho.'})
    except ObjectDoesNotExist:
        return Response({'error': 'Este item não está no seu carrinho.'})  

    
    

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def carrinho(request):
    user = request.user
    order_item = OrderItem.objects.filter(user=user, ordered=False)

    serializer = OrderItemSerializer(order_item, many=True)
    price = 0
    for item in order_item:
        price += item.final_price 


    return Response({'produtos': serializer.data, 'total': price}, status=HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_carrinho_total(request):
    user = request.user
    order_item = OrderItem.objects.filter(user=user, ordered=False)
    price = 0
    return Response({'total': price}, status=HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def create_payment(request):
    order = Order.objects.get(user=request.user, ordered=False)
    stripe.api_key = 'sk_test_51HLxa6H1WKSbV7ewfruiO9CI0AlHu5wyja55rQvQlIYz6krwPPiVCMYy3smvI9C48BQZQ5rlV7Y9r0cQ8adxrJzQ00VtYFUDdU'

    intent = stripe.PaymentIntent.create(
        amount=(int(order.get_total() * 100)),
        currency='brl',
        # Verify your integration in this guide by including this parameter
        metadata={'integration_check': 'accept_a_payment'},
    )

    return Response({'clientSecret': intent['client_secret']}, status=HTTP_200_OK)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def checkout(request):

    produtos = request.data.get('produtos')
    produtos = json.loads(produtos)
    gateway = request.data.get('gateway')
    amount = request.data.get('amount')
    comprovante = request.FILES['comprovante']


    order = Order.objects.get(user=request.user, ordered=False)

    if gateway == 'TR':
        payment = Payment.objects.create(order=order, gateway=gateway, amount=amount, comprovante=comprovante) 

    for produto in produtos:
        order_item = OrderItem.objects.get(pk=produto['pk'])
        
        
        # Verifica se o estoque é gerenciavel
        if order_item.item.has_stock:
            if order_item.item.has_variations:
                item_variation = ItemSize.objects.get(item=order_item.item, size=produto['size'])
                if item_variation.stock >= produto['quantity']:
                    item_variation.stock -= produto['quantity']
                    
                    item_variation.save()

                    order_item.ordered = True
                    order_item.save()

                else:
                    return Response({'error': f'Produto fora de estoque: {produto["item"]}'})
            else:
                if order_item.item.stock >= produto['quantity']:

                    order_item.item.stock -= produto['quantity']
                    order_item.ordered = True
                    
                    
                    order_item.save()
                    order_item.item.save()
        else:
            order_item.ordered = True
            order_item.save()

    order.ordered = True
    order.save()
    return Response({'success': 'Pedido finalizado'})



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def pedidos(request):
    orders = Order.objects.filter(user=request.user, ordered=True)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)