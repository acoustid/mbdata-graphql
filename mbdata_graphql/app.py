from flask import Flask
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy

import mbdata.config as mbdata_config


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("mbdata_graphql.settings")

    db = SQLAlchemy(app)

    mbdata_config.configure(base_class=db.Model, schema=None)
    mbdata_config.freeze()

    from .schema import schema

    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view(
            "graphql",
            schema=schema,
            graphiql=app.config["GRAPHIQL_ENABLED"],
        ),
    )

    @app.cli.command(
        "create-schema",
        help="Initialize the MusicBrainz schema in the target database.",
    )
    def create_schema() -> None:
        db.create_all()

    @app.cli.command(
        "create-sample-data", help="Add sample Musicbrainz data to the target database."
    )
    def create_sample_data() -> None:
        from mbdata.sample_data import create_sample_data

        create_sample_data(db.session)
        db.session.commit()

    return app
