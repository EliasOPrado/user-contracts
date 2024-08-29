import graphene


class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    username = graphene.String()
    email = graphene.String()
    password = graphene.String()  # Password should be handled securely


class ContractInput(graphene.InputObjectType):
    id = graphene.ID()
    description = graphene.String()
    user_id = graphene.ID()
    fidelity = graphene.Int()
    amount = graphene.Decimal()
