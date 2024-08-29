import graphene
from django.contrib.auth.models import User
from user_contracts.models import Contract
from .types import UserType, ContractType


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    all_contracts = graphene.List(ContractType)
    get_user = graphene.Field(UserType, id=graphene.Int(required=True))
    get_contract = graphene.Field(ContractType, id=graphene.Int(required=True))

    def resolve_get_user(self, info, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None

    def resolve_get_contract(self, info, id):
        try:
            return Contract.objects.get(pk=id)
        except Contract.DoesNotExist:
            return None

    def resolve_all_users(self, info):
        return User.objects.all()

    def resolve_all_contracts(self, info):
        return Contract.objects.all()
