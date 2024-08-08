from sqlalchemy import inspect

from speedapi.models import User, metadata_registry


def test_persisted_tables_should_match_with_registered_tables(engine):
    inspector = inspect(subject=engine)

    persisted_tables = set(inspector.get_table_names())
    persisted_tables.discard('alembic_version')
    registered_tables = set(metadata_registry.metadata.tables)

    assert persisted_tables == registered_tables


def test_user_data_should_be_persisted_in_users_table(session, user_template):
    session.add(User(**user_template))
    session.commit()

    retrieved_user = session.get(entity=User, ident=1)

    assert retrieved_user is not None
