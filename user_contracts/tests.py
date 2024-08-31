import graphene
from decimal import Decimal
from django.contrib.auth.models import User
from user_contracts.models import Contract
from user_contracts.api.queries import Query
from user_contracts.api.mutations import Mutation
from user_contracts.api.schema import schema
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase


# Create your tests here.
class GraphqlTestCase(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="password123"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="password123"
        )

        # Create contracts
        self.contract1 = Contract.objects.create(
            description="Contract 1", user=self.user1, fidelity=12, amount=100.50
        )
        self.contract2 = Contract.objects.create(
            description="Contract 2", user=self.user2, fidelity=24, amount=200.75
        )

    def get_object_or_none(self, model_class, **kwargs):
        try:
            return model_class.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    def test_list_users(self):
        query = """
            query {
                allUsers {
                    id
                    username
                    email
                }
            }
        """
        schema = graphene.Schema(query=Query)
        result = schema.execute(query)
        self.assertIsNone(result.errors)
        self.assertIsNotNone(result.data["allUsers"])
        self.assertEqual(result.data["allUsers"][0]["email"], self.user1.email)
        self.assertEqual(result.data["allUsers"][0]["username"], self.user1.username)
        self.assertEqual(result.data["allUsers"][1]["email"], self.user2.email)
        self.assertEqual(result.data["allUsers"][1]["username"], self.user2.username)

    def test_get_user_by_id(self):
        query = f"""
            query {{
                getUser(id: {self.user1.id}) {{
                    id
                    username
                    email
                }}
            }}
        """
        schema = graphene.Schema(query=Query)
        result = schema.execute(query)
        self.assertIsNone(result.errors)
        self.assertIsNotNone(result.data["getUser"])
        self.assertEqual(result.data["getUser"]["id"], str(self.user1.id))
        self.assertEqual(result.data["getUser"]["username"], self.user1.username)
        self.assertEqual(result.data["getUser"]["email"], self.user1.email)

    def test_get_contracts_by_user_id(self):
        pass

    def test_update_user(self):
        query = f"""
            query {{
                getContractsByUserId(id:{self.user1.id}){{
                    id
                    amount
                    description
                    fidelity
                    amount
                    user {{
                    id
                    }}
                }}
            }}
        """
        schema = graphene.Schema(query=Query)
        result = schema.execute(query)
        self.assertIsNone(result.errors)
        self.assertIsNotNone(result.data["getContractsByUserId"])
        self.assertEqual(
            int(result.data["getContractsByUserId"][0]["user"]["id"]), self.user1.id
        )
        self.assertEqual(
            Decimal(result.data["getContractsByUserId"][0]["amount"]),
            self.contract1.amount,
        )
        self.assertEqual(
            result.data["getContractsByUserId"][0]["description"],
            self.contract1.description,
        )

    def test_update_user(self):
        query = f"""
            mutation {{
                updateUser(id: {self.user1.id}, input: {{
                    username: "updateduser",
                    email: "updateduser@example.com",
                    password: "newpassword123"
                }}) {{
                    user {{
                    id
                    username
                    email
                    }}
                    success
                    message
                }}
            }}
        """
        schema = graphene.Schema(mutation=Mutation, query=Query)
        result = schema.execute(query)
        updated_user = User.objects.get(id=self.user1.id)
        self.assertIsNone(result.errors)
        self.assertIsNotNone(result.data["updateUser"])
        self.assertEqual(int(result.data["updateUser"]["user"]["id"]), self.user1.id)
        self.assertEqual(
            result.data["updateUser"]["user"]["username"], updated_user.username
        )
        self.assertEqual(result.data["updateUser"]["user"]["username"], "updateduser")
        self.assertEqual(
            result.data["updateUser"]["message"], "User updated successfully."
        )

    def test_delete_user(self):
        query = f"""
            mutation {{
                deleteUser(id: {self.user1.id}) {{
                    success
                    message
                }}
            }}
        """
        schema = graphene.Schema(mutation=Mutation, query=Query)
        result = schema.execute(query)
        check_deleted_user = self.get_object_or_none(User, id=self.user1.id)
        self.assertIsNone(result.errors)
        self.assertEqual(check_deleted_user, None)
        self.assertIsNotNone(result.data["deleteUser"])
        self.assertEqual(
            result.data["deleteUser"]["message"], "User deleted successfully."
        )

    def test_list_contracts(self):
        query = """
            query {
                allContracts {
                    id
                    description
                    user{
                        id
                    }
                    createdAt
                    fidelity
                    amount
                }
            }
        """
        schema = graphene.Schema(query=Query)
        result = schema.execute(query)
        self.assertIsNone(result.errors)
        self.assertIsNotNone(result.data["allContracts"])
        self.assertEqual(int(result.data["allContracts"][0]["id"]), self.contract1.id)
        self.assertEqual(
            result.data["allContracts"][0]["description"], self.contract1.description
        )
        self.assertEqual(
            int(result.data["allContracts"][0]["user"]["id"]), self.user1.id
        )
        self.assertEqual(
            int(result.data["allContracts"][1]["user"]["id"]), self.user2.id
        )

    def test_get_contract_by_id(self):
        query = f"""
            query {{
                getContractsByUserId(id:{self.user1.id}){{
                    id
                    amount
                    description
                    fidelity
                    amount
                    user {{
                    id
                    }}
                }}
            }}
        """
        result = schema.execute(query)
        self.assertIsNone(result.errors)
        self.assertIsNotNone(result.data["getContractsByUserId"])
        self.assertEqual(
            int(result.data["getContractsByUserId"][0]["user"]["id"]), self.user1.id
        )

    def test_update_contract(self):
        query = f"""
            mutation {{
                updateContract(id: {self.contract1.id}, input: {{
                    description: "Updated contract123",
                    fidelity: 20,
                    amount: "150.00"
                }}) {{
                    contract {{
                    id
                    description
                    user {{
                        id
                    }}
                    createdAt
                    fidelity
                    amount
                    }}
                    message
                        success
                }}
            }}
        """
        schema = graphene.Schema(mutation=Mutation, query=Query)
        result = schema.execute(query)
        updated_contract = Contract.objects.get(id=self.contract1.id)
        self.assertIsNone(result.errors)
        self.assertIsNotNone(result.data["updateContract"])
        self.assertEqual(
            int(result.data["updateContract"]["contract"]["id"]), self.contract1.id
        )
        self.assertEqual(
            result.data["updateContract"]["contract"]["description"],
            updated_contract.description,
        )
        self.assertEqual(
            result.data["updateContract"]["contract"]["description"],
            "Updated contract123",
        )
        self.assertEqual(
            result.data["updateContract"]["message"], "Contract updated successfully."
        )

    def test_delete_contract(self):
        query = f"""
            mutation {{
                deleteContract(id: {self.contract1.id}) {{
                    success
                    message
                }}
            }}
        """
        schema = graphene.Schema(mutation=Mutation, query=Query)
        result = schema.execute(query)
        check_deleted_contract = self.get_object_or_none(Contract, id=self.contract1.id)
        print(result)
        print(check_deleted_contract)
        self.assertIsNone(result.errors)
        self.assertEqual(check_deleted_contract, None)
        self.assertIsNotNone(result.data["deleteContract"])
        self.assertEqual(
            result.data["deleteContract"]["message"], "Contract deleted successfully."
        )
