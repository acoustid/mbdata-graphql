# GraphQL server for accessing MusicBrainz data

The goal of this project is to allow access to a local MusicBrainz database using GraphQL.
It's basically a glue code between [Graphene](https://graphene-python.org/) and [mbdata](https://pypi.org/project/mbdata/).

## Development

Create .env file with the following contents:

    FLASK_ENV=development
    FLASK_DEBUG=true
    FLASK_APP=mbdata_graphql.app:create_app

Run the GraphQL server:

    poetry run flask run

For development purposes, you might want to create a local SQLite database with sample data:

    poetry run flask create-schema
    poetry run flask create-sample-data
