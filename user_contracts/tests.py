import graphene
import json
from decimal import Decimal
from django.contrib.auth.models import User
from user_contracts.models import Contract
from user_contracts.api.queries import Query
from user_contracts.api.mutations import Mutation
from user_contracts.api.schema import schema
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from graphene_django.utils.testing import graphql_query



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

        # Obtain JWT token for authentication
        self.token = self.get_token_for_user(self.user1)

    def get_token_for_user(self, user):
        graphql_url = 'http://localhost:8000/graphql/'  # Update this with your actual URL
        response = self.client.post(graphql_url, json.dumps({
            'query': '''
                mutation {
                    tokenAuth(username: "user1", password: "password123") {
                        token
                    }
                }
            '''
        }), content_type='application/json')

        data = json.loads(response.content)
        return data['data']["tokenAuth"]["token"]

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
        response = self.client.post(
            '/graphql/', 
            json.dumps({'query': query}),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        content = json.loads(response.content)['data']

        self.assertIsNotNone(content['allUsers'])
        self.assertEqual(content['allUsers'][0]['email'], self.user1.email)
        self.assertEqual(content["allUsers"][0]["username"], self.user1.username)
        self.assertEqual(content["allUsers"][1]["email"], self.user2.email)
        self.assertEqual(content["allUsers"][1]["username"], self.user2.username)

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
        response = self.client.post(
            '/graphql/', 
            json.dumps({'query': query}),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        content = json.loads(response.content)['data'] 
        self.assertIsNotNone(content["getUser"])
        self.assertEqual(content["getUser"]["id"], str(self.user1.id))
        self.assertEqual(content["getUser"]["username"], self.user1.username)
        self.assertEqual(content["getUser"]["email"], self.user1.email)

    def test_get_contracts_by_user_id(self):
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
        response = self.client.post(
            '/graphql/', 
            json.dumps({'query': query}),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        content = json.loads(response.content)['data']
        self.assertIsNotNone(content['getContractsByUserId'])
        self.assertEqual(Decimal(content['getContractsByUserId'][0]['amount']), self.contract1.amount)
        self.assertEqual(content['getContractsByUserId'][0]['description'], self.contract1.description)
        self.assertEqual(content['getContractsByUserId'][0]['fidelity'], self.contract1.fidelity)
        self.assertEqual(int(content['getContractsByUserId'][0]['user']['id']), self.user1.id)

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
        response = self.client.post(
            '/graphql/', 
            json.dumps({'query': query}),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        content = json.loads(response.content)['data']

        self.assertIsNotNone(content["getContractsByUserId"])
        self.assertEqual(
            int(content["getContractsByUserId"][0]["user"]["id"]), self.user1.id
        )
        self.assertEqual(
            Decimal(content["getContractsByUserId"][0]["amount"]),
            self.contract1.amount,
        )
        self.assertEqual(
            content["getContractsByUserId"][0]["description"],
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
        response = self.client.post(
            '/graphql/', 
            json.dumps({'query': query}),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        content = json.loads(response.content)['data']
        updated_user = User.objects.get(id=self.user1.id)
        self.assertIsNotNone(content["updateUser"])
        self.assertEqual(int(content["updateUser"]["user"]["id"]), self.user1.id)
        self.assertEqual(
            content["updateUser"]["user"]["username"], updated_user.username
        )
        self.assertEqual(content["updateUser"]["user"]["username"], "updateduser")
        self.assertEqual(
            content["updateUser"]["message"], "User updated successfully."
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
        response = self.client.post(
            '/graphql/', 
            json.dumps({'query': query}),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        content = json.loads(response.content)['data']
        check_deleted_user = self.get_object_or_none(User, id=self.user1.id)
        
        self.assertEqual(check_deleted_user, None)
        self.assertIsNotNone(content["deleteUser"])
        self.assertEqual(
            content["deleteUser"]["message"], "User deleted successfully."
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
        response = self.client.post(
            '/graphql/', 
            json.dumps({'query': query}),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        content = json.loads(response.content)['data']
        self.assertIsNotNone(content["allContracts"])
        self.assertEqual(int(content["allContracts"][0]["id"]), self.contract1.id)
        self.assertEqual(
            content["allContracts"][0]["description"], self.contract1.description
        )
        self.assertEqual(
            int(content["allContracts"][0]["user"]["id"]), self.user1.id
        )
        self.assertEqual(
            int(content["allContracts"][1]["user"]["id"]), self.user2.id
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
        response = self.client.post(
            '/graphql/', 
            json.dumps({'query': query}),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        content = json.loads(response.content)['data']
        self.assertIsNotNone(content["getContractsByUserId"])
        self.assertEqual(
            int(content["getContractsByUserId"][0]["user"]["id"]), self.user1.id
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
        response = self.client.post(
            '/graphql/', 
            json.dumps({'query': query}),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        content = json.loads(response.content)['data']
        updated_contract = Contract.objects.get(id=self.contract1.id)
        self.assertIsNotNone(content["updateContract"])
        self.assertEqual(
            int(content["updateContract"]["contract"]["id"]), self.contract1.id
        )
        self.assertEqual(
            content["updateContract"]["contract"]["description"],
            updated_contract.description,
        )
        self.assertEqual(
            content["updateContract"]["contract"]["description"],
            "Updated contract123",
        )
        self.assertEqual(
            content["updateContract"]["message"], "Contract updated successfully."
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
        response = self.client.post(
            '/graphql/', 
            json.dumps({'query': query}),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        content = json.loads(response.content)['data']
        check_deleted_contract = self.get_object_or_none(Contract, id=self.contract1.id)

        self.assertEqual(check_deleted_contract, None)
        self.assertIsNotNone(content["deleteContract"])
        self.assertEqual(
            content["deleteContract"]["message"], "Contract deleted successfully."
        )
