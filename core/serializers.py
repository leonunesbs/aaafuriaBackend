from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import (
    Sócio,
    Financeiro
)



class SócioSerializer(serializers.ModelSerializer):
    nome_completo = serializers.StringRelatedField()
    class Meta:
        model = Sócio
        fields = ['nome_completo', 'turma', 'matrícula']

class UserSerializer(serializers.ModelSerializer):
    sócio = SócioSerializer()
    class Meta:
        model = User
        fields = ['username', 'email', 'sócio']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class FinanceiroSerializer(serializers.ModelSerializer):
    fluxo = serializers.StringRelatedField(source='get_fluxo_display')
    data_da_movimentação = serializers.DateField(format="%d/%m/%Y")
    class Meta:
        model = Financeiro
        fields = ['pk', 'fluxo', 'finalidade', 'valor', 'observações', 'responsável', 'data_da_movimentação']