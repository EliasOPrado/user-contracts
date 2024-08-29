import graphene
from django.contrib.auth.models import User
from user_contracts.models import Contract
from .inputs import UserInput, ContractInput
from .types import UserType, ContractType


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, input):
        # Create user with a hashed password
        user = User(
            username=input.username,
            email=input.email,
        )
        if input.password:
            user.set_password(input.password)
        user.save()
        return CreateUserMutation(user=user)


class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = UserInput(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, id, input):
        user = User.objects.get(pk=id)
        if input.username:
            user.username = input.username
        if input.email:
            user.email = input.email
        if input.password:
            user.set_password(input.password)
        user.save()
        return UpdateUserMutation(user=user)


class DeleteUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        user = User.objects.get(pk=id)
        user.delete()
        return DeleteUserMutation(success=True)


class CreateContractMutation(graphene.Mutation):
    class Arguments:
        input = ContractInput(required=True)

    contract = graphene.Field(ContractType)

    def mutate(self, info, input):
        user = User.objects.get(pk=input.user_id)
        contract = Contract(
            description=input.description,
            user=user,
            fidelity=input.fidelity,
            amount=input.amount,
        )
        contract.save()
        return CreateContractMutation(contract=contract)


class UpdateContractMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = ContractInput(required=True)

    contract = graphene.Field(ContractType)

    def mutate(self, info, id, input):
        contract = Contract.objects.get(pk=id)
        if input.description:
            contract.description = input.description
        if input.fidelity:
            contract.fidelity = input.fidelity
        if input.amount:
            contract.amount = input.amount
        contract.save()
        return UpdateContractMutation(contract=contract)


class DeleteContractMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        contract = Contract.objects.get(pk=id)
        contract.delete()
        return DeleteUserMutation(success=True)


class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    update_user = UpdateUserMutation.Field()
    delete_user = DeleteUserMutation.Field()

    create_contract = CreateContractMutation.Field()
    update_contract = UpdateContractMutation.Field()
    delete_contract = DeleteContractMutation.Field()
