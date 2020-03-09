import graphene
import tracks.schema # to use the root query of the tracks schema
import users.schema
import graphene
import graphql_jwt

class Query(users.schema.Query, tracks.schema.Query, graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation, tracks.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field() # provide jwt token if the given credentials are correct
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

# create SCHEMA
schema = graphene.Schema(query=Query, mutation=Mutation)
