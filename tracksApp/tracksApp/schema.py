import graphene
import tracks.schema # to use the root query of the tracks schema
import users.schema

class Query(users.schema.Query, tracks.schema.Query, graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation, tracks.schema.Mutation, graphene.ObjectType):
    pass

# create SCHEMA
schema = graphene.Schema(query=Query, mutation=Mutation)
