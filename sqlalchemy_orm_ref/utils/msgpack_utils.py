from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from typing import Optional, Union
from uuid import UUID, uuid4

from core.config import logging_settings
import msgpack

from utils.logger import get_logger

log = get_logger(__name__, level=logging_settings.LOG_LEVEL)

from utils.constants import default_serialize_dir


def msgpack_serialize(
    _json: dict = None, filename: str = None
) -> dict[str, Union[bool, str, dict[str, Union[str, dict]]]]:
    if not _json:
        raise ValueError("Missing Python dict data to serialize")

    if not filename:
        log.debug(f"Missing filename. Generating a random filename.")

        filename = str(uuid4())

    if filename.endswith(".msgpack"):
        filename.replace(".msgpack", "")

    filename = f"{default_serialize_dir}/{filename}.msgpack"

    if _json:
        try:
            with open(f"{filename}", "wb") as outfile:
                packed = msgpack.packb(_json)
                outfile.write(packed)

            return_obj = {
                "success": True,
                "detail": {"message": f"Data serialized to file {filename}"},
            }

        except Exception as exc:
            log.error(
                {"exception": "Unhandled exception writing msgpack."}, exc_info=True
            )

            return_obj = {"success": False, "detail": {"message": f"{exc}"}}

    return return_obj


def msgpack_deserialize(
    filename: str = None,
) -> dict[str, Union[bool, str, dict[str, Union[str, dict]]]]:
    if not filename:
        raise ValueError("Must pass a file name/path to deserialize")

    if not Path(filename).exists():
        raise FileNotFoundError(f"Could not find file: {filename}")

    try:
        with open(f"{filename}", "rb") as infile:
            in_bytes = infile.read()
            unpacked = msgpack.unpackb(in_bytes)

        return_obj = {
            "success": True,
            "detail": {
                "message": f"Data deserialized from file {filename}",
                "unpacked": unpacked,
            },
        }

    except Exception as exc:
        log.error({"exception": "Unhandled exception reading msgpack."}, exc_info=True)

        return_obj = {"success": False, "detail": {"message": f"{exc}"}}

    return return_obj
