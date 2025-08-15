# alx_backend_graphql_crm/schema.py
import graphene

class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info):
        return "Hello, GraphQL!"

schema = graphene.Schema(query=Query)
