import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from user_contracts.models import Contract


class UserType(DjangoObjectType):
    """
    GraphQL type for the User model.

    This class maps the User Django model to a GraphQL type, making it accessible
    in GraphQL queries and mutations.
    """
    class Meta:
        model = User
        field = "__all__"


class ContractType(DjangoObjectType):
    """
    GraphQL type for the Contract model.

    This class maps the User Django model to a GraphQL type, making it accessible
    in GraphQL queries and mutations.
    """
    class Meta:
        model = Contract
        fields = "__all__"
