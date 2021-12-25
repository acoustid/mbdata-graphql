import graphene
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


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()

    artists = SQLAlchemyConnectionField(Artist.connection)
    artist = graphene.Field(Artist, gid=graphene.String(required=True))

    def resolve_artist(self, info, gid: str):
        query = Artist.get_query(info)
        return query.filter_by(gid=gid).first()


schema = graphene.Schema(query=Query)
