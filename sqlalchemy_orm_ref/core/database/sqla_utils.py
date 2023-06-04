"""Custom functions/utilities for SQLAlchemy.

Includes functions to print SQLAlchemy table creation SQL statements,
as well as a MetaData object's table data.
"""
from __future__ import annotations

from typing import Any

import sqlalchemy as sa

## Use with print to demo table SQL, i.e. print(CreateTable(SomeClass.__table__))
from sqlalchemy.schema import CreateTable


def print_sql(_class: Any = None) -> None:
    """Print the SQL generated from a Mapped SQLAlchemy class.

    Put classnames in the Union[] list, and use quotes. This enabled type hinting before
    the class is declared.
    """
    if not _class:
        raise ValueError("Missing class input.")

    print(
        f"Generated SQL for class [{_class.__tablename__}]:\n{CreateTable(_class.__table__)}"
    )


def debug_metadata_obj(metadata_obj: sa.MetaData = None) -> None:
    """
    Debug-print a SQLAlchemy MetaData object.

    Loop over tables and print names.
    """

    if not metadata_obj:
        raise ValueError("Missing a SQLAlchemy metadata object.")

    if not isinstance(metadata_obj, sa.MetaData):
        raise ValueError(
            f"Expected a MetaData obj, not object of type '{type(metadata_obj).__name__}'"
        )

    for _table in metadata_obj.sorted_tables:
        print(f"Table name: {_table.name}")


def create_metadata(metadata_obj: sa.MetaData = None, engine: sa.Engine = None) -> None:
    """
    Accept a SQLalchemy MetaData object, run .create_all(engine) to create
    table metadata.
    """

    if not metadata_obj:
        raise ValueError("Missing a SQLAlchemy MetaData object.")

    if not isinstance(metadata_obj, sa.MetaData):
        raise ValueError(
            f"Expected a MetaData obj, not object of type '{type(metadata_obj).__name__}'"
        )

    if not engine:
        raise ValueError("Missing a SQLAlchemy engine object.")

    if not isinstance(engine, sa.Engine):
        raise ValueError(
            f"Expected a SQLAlchemy engine obj, not object of type '{type(engine).__name__}"
        )

    try:
        metadata_obj.create_all(engine)
    except Exception as exc:
        raise Exception(f"Error creating table metadata. Details: {exc}")
