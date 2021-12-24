from sqlalchemy.orm import Session

from mbdata_graphql.schema import schema


def test_all_artists(db_session: Session) -> None:
    query = """
{
  allArtists(first:3) {
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
    result = schema.execute(query, context_value={'session': db_session})
    assert result.to_dict() == {
        'data': {
            'allArtists': {
                'edges': [],
                'pageInfo': {'endCursor': None, 'hasNextPage': False}
            },
        },
    }
