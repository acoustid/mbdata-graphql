import graphene
from graphene import String, Field, List
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from mbdata import models as mb

import mbdata_graphql.types  # noqa: F401


class Artist(SQLAlchemyObjectType):
    class Meta:
        model = mb.Artist
        interfaces = (graphene.relay.Node,)
        id = "gid"
        exclude_fields = (
            "id",
            "begin_date_year",
            "begin_date_month",
            "begin_date_day",
            "end_date_year",
            "end_date_month",
            "end_date_day",
        )


class Release(SQLAlchemyObjectType):
    class Meta:
        model = mb.Release
        interfaces = (graphene.relay.Node,)
        id = "gid"


class Track(SQLAlchemyObjectType):
    class Meta:
        model = mb.Track
        interfaces = (graphene.relay.Node,)
        id = "gid"


class MediumFormat(SQLAlchemyObjectType):
    class Meta:
        model = mb.MediumFormat
        id = "gid"


class Medium(SQLAlchemyObjectType):
    class Meta:
        model = mb.Medium
        id = "id"

    tracks = List(Track)


class Recording(SQLAlchemyObjectType):
    class Meta:
        model = mb.Recording
        interfaces = (graphene.relay.Node,)
        id = "gid"

    tracks = SQLAlchemyConnectionField(Track)


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()

    artists = SQLAlchemyConnectionField(Artist.connection)
    artist = Field(Artist, gid=String(required=True))

    releases = SQLAlchemyConnectionField(Release.connection)
    release = Field(Release, gid=String(required=True))

    def resolve_artist(self, info, gid: str):
        query = Artist.get_query(info)
        return query.filter_by(gid=gid).first()

    def resolve_release(self, info, gid: str):
        query = Release.get_query(info)
        return query.filter_by(gid=gid).first()


schema = graphene.Schema(query=Query)
