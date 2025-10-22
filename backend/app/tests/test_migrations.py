from sqlalchemy import inspect

def test_core_tables_exist(db_session):
    insp = inspect(db_session.bind)
    tables = set(insp.get_table_names())
    # Adjust to your actual names
    assert "users" in tables
    assert "refresh_tokens" in tables
