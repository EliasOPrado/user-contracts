import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from user_contracts.models import Contract


class UserType(DjangoObjectType):
    class Meta:
        model = User
        field = "__all__"


class ContractType(DjangoObjectType):
    class Meta:
        model = Contract
        fields = "__all__"
