import io
import json

from discord import File


def dict_to_file(profile: dict, filename: str) -> File:
    str_io = io.BytesIO(json.dumps(profile, indent="\t", ensure_ascii=False).encode())
    return File(str_io, filename)
