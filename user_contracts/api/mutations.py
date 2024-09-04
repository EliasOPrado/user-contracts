import graphene
import graphql_jwt
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from user_contracts.models import Contract
from .inputs import UserInput, ContractInput
from .types import UserType, ContractType


class CreateUserMutation(graphene.Mutation):
    """
    Mutation for creating a new user in the GraphQL API.

    This mutation handles the creation of a new user by accepting an input 
    of type `UserInput`. It returns the created user object, a success flag, 
    and a message indicating the result of the operation.
    """
    class Arguments:
        input = UserInput(required=True)

    user = graphene.Field(UserType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, input):
        try:
            user = User.objects.create_user(
                username=input.username, email=input.email, password=input.password
            )
            return CreateUserMutation(
                success=True, message="User created successfully.", user=user
            )
        except ValidationError as e:
            raise GraphQLError(f"Validation error: {str(e)}")
        except Exception as e:
            raise GraphQLError(f"Exception error: {str(e)}")


class UpdateUserMutation(graphene.Mutation):
    """
    Mutation for updating an existing user in the GraphQL API.

    This mutation handles the update of a existing user by accepting an input 
    of type `UserInput` and `graphene.ID`. It returns the updated user object, a success flag, 
    and a message indicating the result of the operation.
    """
    class Arguments:
        id = graphene.ID(required=True)
        input = UserInput(required=True)

    user = graphene.Field(UserType)
    success = graphene.Boolean()
    message = graphene.String()

    @login_required
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
    """
    Mutation for deleting an existing user in the GraphQL API.

    This mutation handles the delete of a existing user by accepting an input 
    of type `graphene.ID`. In addiiton, before trying to delete a user, the code
    will check if the user is attached to a contract. If not, the user will be delete, else
    a message will be displayed not allowing the user to be removed.
    It returns the updated user object, a success flag, 
    and a message indicating the result of the operation.
    """
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, id):
        try:
            user = User.objects.get(pk=id)
            
            # Check if the user is attached to any contracts
            if Contract.objects.filter(user=user).exists():
                raise GraphQLError("Cannot delete user because they are attached to a contract.")
            
            # Proceed with deletion if no contracts are found
            user.delete()
            return DeleteUserMutation(
                success=True, message="User deleted successfully."
            )
        except User.DoesNotExist:
            raise GraphQLError(f"User with ID {id} does not exist.")
        except Exception as e:
            raise GraphQLError(f"Could not delete user: {str(e)}")


class CreateContractMutation(graphene.Mutation):
    """
    Mutation for creating a new contract in the GraphQL API.

    This mutation handles the creation of a new contract by accepting an input 
    of type `ContractInput` attaching an user to it. 
    This mutation also returns the created user object, a success flag, 
    and a message indicating the result of the operation.
    """
    class Arguments:
        input = ContractInput(required=True)

    contract = graphene.Field(ContractType)
    success = graphene.Boolean()
    message = graphene.String()

    @login_required
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
            return CreateContractMutation(
                success=True,
                message="Contract created successfully.",
                contract=contract,
            )
        except User.DoesNotExist:
            raise GraphQLError(
                "You cannot create  a contract with a user that does not exist."
            )
        except Exception as e:
            raise GraphQLError(f"Exception error: {str(e)}")


class UpdateContractMutation(graphene.Mutation):
    """
    Mutation for updating an existing contract in the GraphQL API.

    This mutation handles the update of a existing contract by accepting an input 
    of type `ContractInput` and `graphene.ID`. It returns the updated contract object, a success flag, 
    and a message indicating the result of the operation.
    """
    class Arguments:
        id = graphene.ID(required=True)
        input = ContractInput(required=True)

    contract = graphene.Field(ContractType)
    success = graphene.Boolean()
    message = graphene.String()

    @login_required
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
            return UpdateContractMutation(
                success=True,
                message="Contract updated successfully.",
                contract=contract,
            )
        except Contract.DoesNotExist:
            raise GraphQLError(f"This contract does not exist.")
        except Exception as e:
            raise GraphQLError(f"Exception error: {str(e)}")


class DeleteContractMutation(graphene.Mutation):
    """
    Mutation for deleting an existing contract in the GraphQL API.

    This mutation handles the delete of a existing contract by accepting an input 
    of type `graphene.ID`. It returns the updated user object, a success flag, 
    and a message indicating the result of the operation.
    """
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, id):
        try:
            contract = Contract.objects.get(pk=id)
            contract.delete()
            return DeleteUserMutation(
                success=True, message="Contract deleted successfully."
            )
        except Exception as e:
            raise GraphQLError(f"Exception error: {str(e)}")


class Mutation(graphene.ObjectType):
    """
    The Mutation class represents all the queries that can perform
    server-side data changes.
    """

    # authentication mutations
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    # user mutations
    create_user = CreateUserMutation.Field()
    update_user = UpdateUserMutation.Field()
    delete_user = DeleteUserMutation.Field()

    # contract mutations
    create_contract = CreateContractMutation.Field()
    update_contract = UpdateContractMutation.Field()
    delete_contract = DeleteContractMutation.Field()
