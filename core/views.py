from os import stat
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import request
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND, HTTP_409_CONFLICT)

from ecommerce.models import Order
from ecommerce.serializers import OrderSerializer

from .models import Associação, AssociaçãoCategoria, Financeiro, Sócio
from .serializers import (AssociaçãoCategoriaSerializer, AssociaçãoSerializer,
                          FinanceiroSerializer, SócioSerializer,
                          UserSerializer)


class AuthenticationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        self.permission_classes = [IsAuthenticated]
        if request.user.is_authenticated:
            associação = Associação.objects.filter(sócio=request.user.sócio)
            data = {}
            if associação.exists() and associação.first().is_active:
                data['is_sócio'] = associação.first().is_active
                return Response(data,
                                status=HTTP_200_OK)
            if request.user.is_staff:
                data['is_staff'] = True
            data['is_sócio'] = False
            return Response(data, status=HTTP_200_OK)

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')

        if username == '' or password == '' or username is None or password is None:
            return Response({'error': 'Por favor, forneça usuário e senha.'},
                            status=HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if not user:
            return Response({'error': 'Credenciais inválidas'},
                            status=HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user)

        user_serialized = UserSerializer(user)

        data = {
            'token': token.key,
            'user': user_serialized.data,
            'is_sócio': False,
            'is_staff': user.is_staff
        }

        associação = Associação.objects.filter(sócio=user.sócio)
        if associação.exists():
            data['is_sócio'] = associação.first().is_active

        return Response(data, status=HTTP_200_OK)

    def delete(self, request, format=None):
        try:
            Token.objects.get(user=request.user).delete()
            return Response(status=HTTP_200_OK)
        except TypeError:
            return Response({'error': 'Anonymous'}, status=HTTP_204_NO_CONTENT)


class SejaSócioView(APIView):
    permission_classes = [IsAuthenticated]

    def data_validation(self):
        pass

    def get(self, request, format=None):
        sócio = request.user.sócio
        serializer = SócioSerializer(sócio)
        return Response(serializer.data)

    def post(self, request, format=None):
        nome_completo = request.data.get('nome_completo')
        matrícula = request.data.get('matrícula')
        turma = request.data.get('turma')
        data_de_nascimento = request.data.get('data_de_nascimento')
        cpf = request.data.get('cpf')
        email = request.data.get('email')
        celular = request.data.get('celular')

        try:
            foto = request.FILES['foto']
        except:
            return Response({'error': 'Escolha uma foto'}, status=HTTP_400_BAD_REQUEST)

        if not (
            nome_completo and
            matrícula and
            turma and
            data_de_nascimento and
            cpf and
            email and
            celular
        ):
            return Response({'error': 'Todos os campos são obrigatórios'}, status=HTTP_400_BAD_REQUEST)

        sócio = Sócio.objects.get(user=request.user)
        sócio.nome_completo = nome_completo
        sócio.matrícula = matrícula
        sócio.turma = turma
        sócio.data_de_nascimento = data_de_nascimento
        sócio.cpf = cpf
        sócio.email = email
        sócio.celular = celular
        sócio.foto = foto
        sócio.save()

        serializer = SócioSerializer(sócio)

        return Response(serializer.data, status=HTTP_200_OK)


class AssociaçãoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        ass = Associação.objects.filter(sócio=request.user.sócio)
        if ass.exists():
            return Response(status=HTTP_200_OK)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        comprovante = request.FILES['comprovante']
        categoria = request.data.get('categoria')
        conta_destino = request.data.get('conta_destino')

        cat = AssociaçãoCategoria.objects.get(duração=categoria)

        Associação.objects.get_or_create(
            sócio=request.user.sócio,
            categoria=cat,
            comprovante=comprovante,
            conta_destino=conta_destino
        )

        serializer = AssociaçãoCategoriaSerializer(cat)
        return Response(serializer.data, status=HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAdminUser,))
def get_admin_associação(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10

    ass = Associação.objects.all().order_by('-created_date')

    result = paginator.paginate_queryset(ass, request)
    serializer = AssociaçãoSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAdminUser,))
def toggle_associação(request, pk):
    ass = Associação.objects.get(pk=pk)
    ass.is_active = not ass.is_active
    ass.save()
    return Response({'is_active': ass.is_active}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def cadastro(request):
    min_len_pass = 6

    nome = request.data.get('nome')
    email = request.data.get('email')
    matrícula = request.data.get('matrícula')
    turma = request.data.get('turma')
    senha = request.data.get('senha')
    senha_again = request.data.get('senha_again')
    data_de_nascimento = request.data.get('data_de_nascimento')
    is_sócio = request.data.get('is_sócio')
    celular = request.data.get('celular')

    email = email.lower()

    if not (nome and email and matrícula and turma and senha and senha_again and data_de_nascimento and celular):
        return Response({'error': 'Todos os campos são obrigatórios'},
                        status=HTTP_400_BAD_REQUEST)

    if matrícula and not matrícula.isnumeric():
        return Response({'error': 'Sua matrícula deve conter apenas números'},
                        status=HTTP_400_BAD_REQUEST)

    if len(matrícula) != 8:
        return Response({'error': 'Sua matrícula deve conter 8 dígitos'})

    if senha != senha_again:
        return Response({'error': 'As senhas não correspondem'},
                        status=HTTP_400_BAD_REQUEST)

    if len(senha) < min_len_pass:
        return Response(
            {
                'error':
                f'Sua senha deve conter pelo menos {min_len_pass} dígitos'
            },
            status=HTTP_400_BAD_REQUEST)

    if (int(turma) < 9 or int(turma) > 99):
        return Response({'error': 'Turma inválida'},
                        status=HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(username=matrícula,
                                        email=email,
                                        password=senha)
    except:
        return Response({'error': 'Sua matrícula já se encontra cadastrada'},
                        status=HTTP_409_CONFLICT)

    if is_sócio == 'true':
        ass = Associação.objects.create(
            sócio=user.sócio,
            categoria=AssociaçãoCategoria.objects.get(duração='S'),
            is_active=True
        )

    user.sócio.nome_completo = nome
    user.sócio.email = email
    user.sócio.data_de_nascimento = data_de_nascimento
    user.sócio.matrícula = matrícula
    user.sócio.turma = turma
    user.sócio.celular = celular
    user.sócio.save()
    user.save()

    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def reauthenticate(request):
    tk = request.data.get('token')
    try:
        token = Token.objects.get(key=tk)
        return Response({'token': token.key}, status=HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'error': 'Credenciais inválidas'},
                        status=HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def pedidos_user(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10

    orders = Order.objects.filter(
        user=request.user, ordered=True).order_by('-ordered_date')

    result = paginator.paginate_queryset(orders, request)
    serializer = OrderSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def pedidos_admin(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10

    orders = Order.objects.filter(ordered=True).order_by('-ordered_date')

    result = paginator.paginate_queryset(orders, request)
    serializer = OrderSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAdminUser, ))
def status_pedido_admin(request):
    pk = request.data.get('pk')
    status = request.data.get('status')

    order = Order.objects.get(pk=pk)
    order.status = status
    order.save()

    return Response(status=HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def financeiro(request):
    paginator = PageNumberPagination()
    paginator.page_size = 5

    financeiro = Financeiro.objects.all().order_by('-data_da_movimentação')

    result = paginator.paginate_queryset(financeiro, request)
    serializer = FinanceiroSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def financeiro_last_in(request):

    financeiro = Financeiro.objects.filter(
        fluxo='E').order_by('-data_da_movimentação')
    financeiro = financeiro.first()

    serializer = FinanceiroSerializer(financeiro)
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def financeiro_last_out(request):
    financeiro = Financeiro.objects.filter(
        fluxo='S').order_by('-data_da_movimentação')
    financeiro = financeiro.first()

    serializer = FinanceiroSerializer(financeiro)
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAdminUser, ))
def financeiro_entries(request):
    fluxo = request.data.get('fluxo')
    finalidade = request.data.get('finalidade')
    valor = request.data.get('valor')
    observações = request.data.get('observações')
    responsável = request.data.get('responsável')
    data_da_movimentação = request.data.get('data_da_movimentação')

    financeiro = Financeiro.objects.create(
        fluxo=fluxo,
        finalidade=finalidade,
        valor=valor,
        observações=observações,
        responsável=responsável,
        data_da_movimentação=data_da_movimentação,
    )

    return Response(status=HTTP_200_OK)
