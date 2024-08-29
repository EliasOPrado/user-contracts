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


# query
class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    all_contracts = graphene.List(ContractType)

    def resolve_all_users(self, info):
        return User.objects.all()

    def resolve_all_contracts(self, info):
        return Contract.objects.all()
