from sqlalchemy.orm import Session

from mbdata_graphql.schema import schema


def test_release_type(db_session: Session) -> None:
    query_string = """
    {
      __type(name: "Release") {
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
    assert result.data["__type"]["name"] == "Release"
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

    assert find_field("mediums") == {
        "name": "mediums",
        "type": {
            "name": None,
            "kind": "LIST",
            "ofType": {"kind": "OBJECT", "name": "Medium"},
        },
    }


def test_track_type(db_session: Session) -> None:
    query_string = """
    {
      __type(name: "Track") {
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
    assert result.data["__type"]["name"] == "Track"
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

    assert find_field("position") == {
        "name": "position",
        "type": {
            "name": None,
            "kind": "NON_NULL",
            "ofType": {"kind": "SCALAR", "name": "Int"},
        },
    }

    assert find_field("recording") == {
        "name": "recording",
        "type": {
            "name": "Recording",
            "kind": "OBJECT",
            "ofType": None,
        },
    }


def test_medium_type(db_session: Session) -> None:
    query_string = """
    {
      __type(name: "Medium") {
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
    assert result.data["__type"]["name"] == "Medium"
    assert result.data["__type"]["kind"] == "OBJECT"

    def find_field(field_name: str) -> dict:
        for field in result.data["__type"]["fields"]:
            if field["name"] == field_name:
                return field
        assert False, f"Field {field_name} not found"

    assert find_field("position") == {
        "name": "position",
        "type": {
            "name": None,
            "kind": "NON_NULL",
            "ofType": {"kind": "SCALAR", "name": "Int"},
        },
    }

    assert find_field("trackCount") == {
        "name": "trackCount",
        "type": {
            "name": None,
            "kind": "NON_NULL",
            "ofType": {"kind": "SCALAR", "name": "Int"},
        },
    }

    assert find_field("format") == {
        "name": "format",
        "type": {
            "name": "MediumFormat",
            "kind": "OBJECT",
            "ofType": None,
        },
    }

    assert find_field("tracks") == {
        "name": "tracks",
        "type": {
            "name": None,
            "kind": "LIST",
            "ofType": {"kind": "OBJECT", "name": "Track"},
        },
    }

    assert find_field("release") == {
        "name": "release",
        "type": {
            "name": "Release",
            "kind": "OBJECT",
            "ofType": None,
        },
    }


def test_get_release(db_session: Session) -> None:
    query_string = """
    {
      release(gid:"89b1b3ca-07cd-4f67-b9a7-3a3ba86d7149") {
        gid
        name
        mediums {
          position
          trackCount
          format {
            name
          }
          tracks {
            position
            name
            recording {
              gid
            }
          }
        }
      }
    }
    """
    result = schema.execute(query_string, context_value={"session": db_session})
    assert result.errors is None
    assert result.data == {
        "release": {
            "gid": "89b1b3ca-07cd-4f67-b9a7-3a3ba86d7149",
            "mediums": [
                {
                    "format": {"name": "CD"},
                    "position": 1,
                    "trackCount": 12,
                    "tracks": [
                        {
                            "name": "Small Piano Piece",
                            "position": 1,
                            "recording": {
                                "gid": "77ef7468-e8f8-4447-9c7e-52b11272c6cc"
                            },
                        },
                        {
                            "name": "Fantomes",
                            "position": 2,
                            "recording": {
                                "gid": "e6d2be9c-06b7-4a64-911d-076ad4e79c6f"
                            },
                        },
                        {
                            "name": "The Very Last Resort",
                            "position": 3,
                            "recording": {
                                "gid": "1f0a5382-83a4-4570-b24a-897014826867"
                            },
                        },
                        {
                            "name": "Miss You",
                            "position": 4,
                            "recording": {
                                "gid": "98955d91-27fc-4a6c-baf9-8cdb87491814"
                            },
                        },
                        {
                            "name": "De Carla a Pered",
                            "position": 5,
                            "recording": {
                                "gid": "c14c0467-edcb-483b-891e-555776fff31c"
                            },
                        },
                        {
                            "name": "Una",
                            "position": 6,
                            "recording": {
                                "gid": "4a9caecb-bb01-4ac0-b9e6-2e7613c0317b"
                            },
                        },
                        {
                            "name": "Snowflake",
                            "position": 7,
                            "recording": {
                                "gid": "7fb5de20-ce10-48e6-b61c-0101192c5a51"
                            },
                        },
                        {
                            "name": "Concentration (version 3)",
                            "position": 8,
                            "recording": {
                                "gid": "b52e86aa-4481-432c-a5ac-9f830cfcb2a8"
                            },
                        },
                        {
                            "name": "Evil Dub",
                            "position": 9,
                            "recording": {
                                "gid": "f21b457c-464f-4544-9106-870e0b68323b"
                            },
                        },
                        {
                            "name": "Ghost Town",
                            "position": 10,
                            "recording": {
                                "gid": "9a94277f-fc62-4e12-ba14-1354ddb39143"
                            },
                        },
                        {
                            "name": "Dubby Games",
                            "position": 11,
                            "recording": {
                                "gid": "94fb758f-5ec5-4c35-91d1-b8f94b877ecb"
                            },
                        },
                        {
                            "name": "Nightwalker",
                            "position": 12,
                            "recording": {
                                "gid": "54b7b412-fc69-4fc7-8c96-17800eda3a98"
                            },
                        },
                    ],
                },
                {
                    "format": {"name": "CD"},
                    "position": 2,
                    "trackCount": 13,
                    "tracks": [
                        {
                            "name": "Moan (feat. Ane Trolle)",
                            "position": 1,
                            "recording": {
                                "gid": "6b4bc5f4-ffea-4eb0-971b-cbc130a15519"
                            },
                        },
                        {
                            "name": "Break on Through (Dark Ride dub mix)",
                            "position": 2,
                            "recording": {
                                "gid": "910552ed-94ed-48f9-b87f-7133d4e546fa"
                            },
                        },
                        {
                            "name": "The Fallen (Justice remix)",
                            "position": 3,
                            "recording": {
                                "gid": "f0e7f5e3-a59f-4f46-b828-e6dcaca5638a"
                            },
                        },
                        {
                            "name": "Nanny Nanny Boo Boo (Junior Senior remix)",
                            "position": 4,
                            "recording": {
                                "gid": "483dc8c2-93d6-4a3c-a07a-3a2244e7e343"
                            },
                        },
                        {
                            "name": "Contort Yourself",
                            "position": 5,
                            "recording": {
                                "gid": "3af60ae0-abf9-41b1-971c-e1560441410d"
                            },
                        },
                        {
                            "name": "Someone Like You",
                            "position": 6,
                            "recording": {
                                "gid": "cd25d8ee-9cbd-40c7-891c-9dc68384e335"
                            },
                        },
                        {
                            "name": "High on You",
                            "position": 7,
                            "recording": {
                                "gid": "4549104e-18e1-4006-af43-7b973d995025"
                            },
                        },
                        {
                            "name": "Go! (Trentemøller remix)",
                            "position": 8,
                            "recording": {
                                "gid": "79e29af0-5dda-4ac9-a0a8-43ba8f31efa0"
                            },
                        },
                        {
                            "name": "Silent Shout (Trente short edit)",
                            "position": 9,
                            "recording": {
                                "gid": "e2c36349-6092-4b26-8eec-40c5a3c89e54"
                            },
                        },
                        {
                            "name": "Feelin' Good (Trentemøller remix)",
                            "position": 10,
                            "recording": {
                                "gid": "cc58b376-53a0-41a2-9a6d-a569b81228b5"
                            },
                        },
                        {
                            "name": "Beau Mot Plage (Freeform Five remix re-edit)",
                            "position": 11,
                            "recording": {
                                "gid": "a0484b13-1136-47b3-9950-7c2633d989d7"
                            },
                        },
                        {
                            "name": "Always Something Better (feat. Richard Davis)",
                            "position": 12,
                            "recording": {
                                "gid": "e2191030-6274-4a14-9491-30782cc23525"
                            },
                        },
                        {
                            "name": "We Share Our Mother's Health "
                            "(Trentemøller remix)",
                            "position": 13,
                            "recording": {
                                "gid": "be80f050-1549-4a3e-8a65-5d28e14b1a20"
                            },
                        },
                    ],
                },
            ],
            "name": "Trentemøller: The Pølar Mix",
        }
    }


def test_list_releases(db_session: Session) -> None:
    query = """
    {
      releases(first:3) {
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
            "releases": {
                "edges": [
                    {
                        "node": {
                            "gid": "89b1b3ca-07cd-4f67-b9a7-3a3ba86d7149",
                            "name": "Trentemøller: The Pølar Mix",
                        },
                        "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
                    },
                    {
                        "node": {
                            "gid": "7643ee96-fe19-4b76-aa9a-e8af7d0e9d73",
                            "name": "XVI Reflections on Classical Music",
                        },
                        "cursor": "YXJyYXljb25uZWN0aW9uOjE=",
                    },
                ],
                "pageInfo": {
                    "endCursor": "YXJyYXljb25uZWN0aW9uOjE=",
                    "hasNextPage": False,
                },
            }
        }
    }
