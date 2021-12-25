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

    assert find_field("tracks") == {
        "name": "tracks",
        "type": {
            "name": "TrackConnection",
            "kind": "OBJECT",
            "ofType": None,
        },
    }
