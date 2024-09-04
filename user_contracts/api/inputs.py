import graphene


class UserInput(graphene.InputObjectType):
    """
    Input object type for user-related mutations in the GraphQL API.

    This class defines the structure of the input data that can be passed 
    to create or update a user. It includes fields for the user's ID, 
    username, email, and password.
    """
    id = graphene.ID()
    username = graphene.String()
    email = graphene.String()
    password = graphene.String()  # Password should be handled securely


class ContractInput(graphene.InputObjectType):
    """
    Input object type for contract-related mutations in the GraphQL API.

    This class defines the structure of the input data that can be passed 
    to create or update a contract. It includes fields for the contract's ID, 
    description, associated user's ID, fidelity level, and amount.
    """
    id = graphene.ID()
    description = graphene.String()
    user_id = graphene.ID()
    fidelity = graphene.Int()
    amount = graphene.Decimal()
