from sqlalchemy.orm import Session

from mbdata_graphql.schema import schema


def test_recording_type(db_session: Session) -> None:
    query_string = """
    {
      __type(name: "Recording") {
        name
        kind
        fields {
          name
          type {
            name
            kind
            ofType {
              name
              kind
            }
          }
        }
      }
    }
    """
    result = schema.execute(query_string, context_value={"session": db_session})
    assert result.errors is None
    assert result.data["__type"]["name"] == "Recording"
    assert result.data["__type"]["kind"] == "OBJECT"

    def find_field(field_name: str) -> dict:
        for field in result.data["__type"]["fields"]:
            if field["name"] == field_name:
                return field
        assert False, f"Field {field_name} not found"

    assert find_field("gid") == {
        "name": "gid",
        "type": {
            "name": None,
            "kind": "NON_NULL",
            "ofType": {"kind": "SCALAR", "name": "String"},
        },
    }

    assert find_field("name") == {
        "name": "name",
        "type": {
            "name": None,
            "kind": "NON_NULL",
            "ofType": {"kind": "SCALAR", "name": "String"},
        },
    }


def test_get_recording(db_session: Session) -> None:
    query_string = """
    {
      recording(gid: "7fb5de20-ce10-48e6-b61c-0101192c5a51") {
        gid
        name
        length
      }
    }
    """
    result = schema.execute(query_string, context_value={"session": db_session})
    assert result.errors is None
    assert result.data == {
        "recording": {
            "gid": "7fb5de20-ce10-48e6-b61c-0101192c5a51",
            "length": 447026,
            "name": "Snowflake",
        }
    }


def test_get_recording_with_tracks(db_session: Session) -> None:
    query_string = """
    {
      recording(gid: "7fb5de20-ce10-48e6-b61c-0101192c5a51") {
        gid
        name
        length
        tracks {
          pageInfo {
            hasNextPage
          }
          edges {
            cursor
            node {
              position
              medium {
                position
                release {
                  gid
                  name
                }
              }
            }
          }
        }
      }
    }
    """
    result = schema.execute(query_string, context_value={"session": db_session})
    assert result.errors is None
    assert result.data == {
        "recording": {
            "gid": "7fb5de20-ce10-48e6-b61c-0101192c5a51",
            "name": "Snowflake",
            "length": 447026,
            "tracks": {
                "pageInfo": {"hasNextPage": False},
                "edges": [
                    {
                        "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
                        "node": {
                            "position": 7,
                            "medium": {
                                "position": 1,
                                "release": {
                                    "gid": "89b1b3ca-07cd-4f67-b9a7-3a3ba86d7149",
                                    "name": "Trentemøller: The Pølar Mix",
                                },
                            },
                        },
                    }
                ],
            },
        }
    }
