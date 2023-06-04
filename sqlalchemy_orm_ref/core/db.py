"""
SQLAlchemy common database code.

Contains SQLAlchemy setup code, engine, and session(s). Uses dataclasses to define
database connection, and builds a default engine & session. The use of dataclasses is
to minimize depdencies for this common SQLAlchemy code so it can be easily re-used in
other projects utilizing SQLAlchemy for database operations.

The default engine and session are customizable using the get_engine() and get_session()
functions. These functions can be imported & called from another app, with customized
values to control engine & session behavior.

Currently supported databases:
    - [x] SQLite
    - [ ] Postgres
    - [ ] MySQL
    - [ ] MSSQL
    - [ ] Azure Cosmos
    
Be sure to import the Base object from this script and run Base.metadata.create_all(bind=engine)
as early as possible. For example, import the Base object from this script into main.py,
create/import an engine, and immediately run the metadata create function.
"""

from pathlib import Path
from typing import Union
from dataclasses import dataclass, field

import sqlalchemy as sa
from sqlalchemy import orm as sa_orm
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

## Import SQLAlchemy Base object
from core.database.sqla_base import Base

## Import database connection classes
from core.database.sqla_connection_models import saSQLiteConnection


## List of valid/supported databases
valid_db_types: list[str] = ["sqlite"]


## Ensure a supported database is used
def validate_db_type(in_str: str = None) -> bool:
    """
    Validate db_type string in functions that utilize db_type.
    """
    if not in_str:
        raise ValueError("Missing input string to validate")

    if not in_str in valid_db_types:
        return False

    return True


## Create a default SQLite connection
default_conn: saSQLiteConnection = saSQLiteConnection(database="test.sqlite")


def get_engine(
    connection: Union[saSQLiteConnection, str] = default_conn,
    db_type: str = "sqlite",
    echo: bool = False,
) -> sa.Engine:
    """
    Return a SQLAlchemy Engine object.

    https://docs.sqlalchemy.org/en/20/tutorial/engine.html

    To use a database other than SQLite, i.e. Postgres or MySQL, pass
    the lowercase string name of the database.

    Currently supported:
        - [x] SQLite
        - [ ] Postgres
        - [ ] MySQL
        - [ ] MSSQL
        - [ ] Azure Cosmos
    """
    if not connection:
        raise ValueError("Missing connection object/string.")

    if isinstance(connection, str):
        if db_type == "sqlite":
            connection: saSQLiteConnection = saSQLiteConnection(database=connection)

    ## Validate db_type input
    if db_type:
        _valid: bool = validate_db_type(db_type)

        if not _valid:
            raise ValueError(
                f"Invalid db_type: {db_type}. Must be one of: {valid_db_types}"
            )

    else:
        ## Default to sqlite if no db_type is passed
        db_type = "sqlite"

    if db_type == "sqlite":
        ## Ensure path to database file exists
        connection.ensure_path()

    try:
        engine = create_engine(connection.connection_string, echo=echo)
    except Exception as exc:
        raise Exception(f"Unhandled exception creating database engine. Details: {exc}")
    finally:
        return engine


## Create a default engine
default_engine: sa.Engine = get_engine()


def get_session(
    engine: sa.Engine = None,
    autoflush: bool = False,
    expire_on_commit: bool = False,
    class_=Session,
) -> sessionmaker[Session]:
    """
    Factory for creating SQLAlchemy sessions.

    Returns a sqlalchemy.orm.sessionmaker Session instance. Import this
    function in scripts that interact with the database, and create a
    SessionLocal object with SessionLocal = get_session(**args)
    """
    try:
        _sess = sessionmaker(
            bind=engine,
            autoflush=autoflush,
            expire_on_commit=expire_on_commit,
            class_=class_,
        )
    except Exception as exc:
        raise Exception(
            f"Unhandled exception creating a sessionmaker Session. Details: {exc}"
        )
    finally:
        return _sess


## Default database session object
DefaultSession: sessionmaker[Session] = get_session()
