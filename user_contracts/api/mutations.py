import graphene
from graphql import GraphQLError
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from user_contracts.models import Contract
from .inputs import UserInput, ContractInput
from .types import UserType, ContractType


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    user = graphene.Field(UserType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, input):
        try:
            user = User.objects.create_user(
                username=input.usernane, email=input.email, password=input.password
            )
            return CreateUserMutation(
                success=True, message="User created successfully.", user=user
            )
        except ValidationError as e:
            raise GraphQLError(f"Validation error: {str(e)}")
        except Exception as e:
            raise GraphQLError(f"Exception error: {str(e)}")


class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = UserInput(required=True)

    user = graphene.Field(UserType)
    sucess = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id, input):
        try:
            user = User.objects.get(pk=id)
            if input.username:
                user.username = input.username
            if input.email:
                user.email = input.email
            if input.password:
                user.set_password(input.password)
            user.save()
            return UpdateUserMutation(
                success=True, message="User updated successfully.", user=user
            )
        except Exception as e:
            raise GraphQLError(f"Could not update user: {str(e)}")


class DeleteUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            user = User.objects.get(pk=id)
            user.delete()
            return DeleteUserMutation(success=True)
        except Exception as e:
            raise GraphQLError(f"Could not delete user: {str(e)}")


class CreateContractMutation(graphene.Mutation):
    class Arguments:
        input = ContractInput(required=True)

    contract = graphene.Field(ContractType)

    def mutate(self, info, input):
        try:
            user = User.objects.get(pk=input.user_id)
            contract = Contract(
                description=input.description,
                user=user,
                fidelity=input.fidelity,
                amount=input.amount,
            )
            contract.save()
            return CreateContractMutation(contract=contract)
        except User.DoesNotExist:
            raise GraphQLError(
                "You cannot create  a contract with a user that does not exist."
            )
        except Exception as e:
            raise GraphQLError(f"Exception error: {str(e)}")


class UpdateContractMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = ContractInput(required=True)

    contract = graphene.Field(ContractType)

    def mutate(self, info, id, input):
        try:
            contract = Contract.objects.get(pk=id)
            if input.description:
                contract.description = input.description
            if input.fidelity:
                contract.fidelity = input.fidelity
            if input.amount:
                contract.amount = input.amount
            contract.save()
            return UpdateContractMutation(contract=contract)
        except Contract.DoesNotExist:
            raise GraphQLError(f"This contract does not exist.")
        except Exception as e:
            raise GraphQLError(f"Exception error: {str(e)}")


class DeleteContractMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            contract = Contract.objects.get(pk=id)
            contract.delete()
            return DeleteUserMutation(success=True)
        except Exception as e:
            raise GraphQLError(f"Exception error: {str(e)}")


class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    update_user = UpdateUserMutation.Field()
    delete_user = DeleteUserMutation.Field()

    create_contract = CreateContractMutation.Field()
    update_contract = UpdateContractMutation.Field()
    delete_contract = DeleteContractMutation.Field()
