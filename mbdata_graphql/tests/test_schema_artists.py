from sqlalchemy.orm import Session

from mbdata_graphql.schema import schema


def test_get_artist(db_session: Session) -> None:
    query = """
    {
      artist(gid: "8970d868-0723-483b-a75b-51088913d3d4") {
        gid
        name
        sortName
        comment
      }
    }
    """
    result = schema.execute(query, context_value={"session": db_session})
    assert result.to_dict() == {
        "data": {
            "artist": {
                "gid": "8970d868-0723-483b-a75b-51088913d3d4",
                "name": "Moby",
                "sortName": "Moby",
                "comment": "electronic musician Richard Melville Hall",
            },
        },
    }


def test_get_artist_not_found(db_session: Session) -> None:
    query = """
    {
      artist(gid: "ebf69959-e059-496e-bb67-518139df8c23") {
        gid
        name
        sortName
        comment
      }
    }
    """
    result = schema.execute(query, context_value={"session": db_session})
    assert result.to_dict() == {
        "data": {
            "artist": None,
        },
    }


def test_get_artists(db_session: Session) -> None:
    query = """
{
  artists(first:3) {
    edges	{
      node {
        gid
        name
      }
      cursor
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
    """
    result = schema.execute(query, context_value={"session": db_session})
    assert result.to_dict() == {
        "data": {
            "artists": {
                "edges": [
                    {
                        "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
                        "node": {
                            "gid": "89ad4ac3-39f7-470e-963a-56509c546377",
                            "name": "Various Artists",
                        },
                    },
                    {
                        "cursor": "YXJyYXljb25uZWN0aW9uOjE=",
                        "node": {
                            "gid": "2d67239c-aa40-4ad5-a807-9052b66857a6",
                            "name": "Le Tigre",
                        },
                    },
                    {
                        "cursor": "YXJyYXljb25uZWN0aW9uOjI=",
                        "node": {
                            "gid": "8970d868-0723-483b-a75b-51088913d3d4",
                            "name": "Moby",
                        },
                    },
                ],
                "pageInfo": {
                    "endCursor": "YXJyYXljb25uZWN0aW9uOjI=",
                    "hasNextPage": True,
                },
            }
        }
    }
