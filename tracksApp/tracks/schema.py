# schema of tracks application
import graphene
from graphene_django import DjangoObjectType # to inherit the DjangoObjectType
from .models import Track  # to tell graphene_django about the shape of the tracks data

class TrackType(DjangoObjectType):
    class Meta:
        model = Track # tell TrackType to inherit Track model

class Query(graphene.ObjectType): # root query class
    tracks = graphene.List(TrackType) # create track query to get all tracks as a checklist

    def resolve_tracks(self, info): # resolve the query
        return Track.objects.all()

# mutation in createTrack class
class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType) # return created track on a track field

    class Arguments: # provide inner arg class
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, title, description, url): # resolver function that store the var and persist it into db, return the class instance
        track = Track(title=title, description=description, url=url)
        track.save()
        return CreateTrack(track=track)

# root mutation class
class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
