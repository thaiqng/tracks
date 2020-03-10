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
        title = graphene.String(required=True)
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, title, description=None, url=None): # resolver function that store the var and persist it into db, return the class instance
        user = info.context.user or None # get info about the user
        track = Track(title=title, description=description, url=url, posted_by=user)

        # soft crash by raising exception if not authenticated
        if user.is_anonymous:
            raise Exception("Sign in to add a track!")

        track.save()
        return CreateTrack(track=track)

# update track class
class UpdateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments: # provide inner arg class
        track_id = graphen.Int(required=True)
        title = graphene.String(required=True)
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, track_id, title, description=None, url=None):
        user = info.context.user
        track = Track.objects.get(id=track_id)

        if track.posted_by != user:
            raise Exception("Not allowed to update this track!")

        track.title = title
        track.description = description
        track.url = url
        track.save()
        return UpdateTrack(track=track)

# track mutation class
class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()
