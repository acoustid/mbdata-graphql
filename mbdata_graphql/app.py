from flask import Flask
from flask_graphql import GraphQLView

from .schema import schema


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('mbdata_graphql.settings')

    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=app.config['GRAPHIQL_ENABLED'],
        )
    )

    return app
