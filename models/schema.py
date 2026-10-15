from sqlalchemy import Engine, inspect, text


def upgrade_schema(engine: Engine) -> None:
    """Add columns introduced after a table was first created by create_all.

    create_all never alters existing tables, so databases created before the
    admin role existed need the column added in place.
    """
    inspector = inspect(engine)
    if "users" not in inspector.get_table_names():
        return
    columns = {column["name"] for column in inspector.get_columns("users")}
    if "is_admin" not in columns:
        with engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT FALSE")
            )
