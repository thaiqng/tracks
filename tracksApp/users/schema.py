from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType

# create new user with graphql Mutation
class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    me = graphene.Field(UserType) # store authenticated status

    def resolve_user(self, info, id):
        return get_user_model().objects.get(id=id)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous: # if use is not authenticated
            raise Exception("Not signed in!") # to prevent this exception must pass through a valid jwt token on an auth header when sending a request to execute a graphql operation i.e. because can access must execute token_auth mutation (signed up)
        return user

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()
        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

# query individual user based on their id
