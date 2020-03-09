import graphene
import tracks.schema # to use the root query of the tracks schema

class Query(tracks.schema.Query, graphene.ObjectType):
    pass

# create SCHEMA
schema = graphene.Schema(query=Query)