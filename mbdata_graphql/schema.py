import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from mbdata import models as mb

import mbdata_graphql.types


class Artist(SQLAlchemyObjectType):
    class Meta:
        model = mb.Artist


class Query(graphene.ObjectType):
    artists = graphene.List(Artist)

    def resolve_artists(self, info):
        query = Artist.get_query(info)
        return query.all()


schema = graphene.Schema(query=Query)
