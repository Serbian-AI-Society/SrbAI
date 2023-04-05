import pickle
from typing import Any


def serialize_object(obj: Any, path: str) -> None:
    """
    Serializes object first to a pickle string then encodes that string into base64.
    """
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def deserialize_object(path: str) -> Any:
    """
    Deserializes object encoded in base64 made from a pickle string.
    Assumes path exists.
    """
    with open(path, "rb") as f:
        obj = pickle.load(f)

    return obj


def open_corpus(path: str) -> str:
    """
    Opens a corpus and loads its content into a string.
    Assumes path exists.
    """
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    return content
