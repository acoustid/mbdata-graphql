# GraphQL server for accessing MusicBrainz data

The goal of this project is to allow access to a local MusicBrainz database using GraphQL.
It's basically a glue code between [Graphene](https://graphene-python.org/) and [mbdata](https://pypi.org/project/mbdata/).

Run the GraphQL server locally for development purposes:

    FLASK_DEBUG=1 FLASK_APP=mbdata_graphql.app:create_app poetry run flask run
