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
