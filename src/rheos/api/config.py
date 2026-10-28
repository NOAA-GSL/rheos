import os
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path

from uwtools.api.config import compose as uw_compose
from uwtools.api.config import compose_to_dict as uw_compose_to_dict
from uwtools.config.formats.base import Config

from rheos.util import pkgname


def catalog() -> list[str]:
    """
    Catalog available config resources as slash-separated paths relative to the config resources
    root.
    """
    return sorted(_walk(resources.files(f"{pkgname}.resources.config"), []))


def compose(configs: list[str], *, quiet: bool = False, realize: bool = False) -> Config:
    """
    Compose the given configs, writing the result to stdout unless quiet.
    """
    if quiet:
        return uw_compose(configs, output_file=Path(os.devnull), realize=realize)
    return uw_compose(configs, realize=realize)


def compose_to_dict(configs: list[str]) -> dict:
    """
    Compose the given configs and return the result as a dict.
    """
    return uw_compose_to_dict(configs)


def extract(key_path: list[str]) -> str:
    """
    Return the text of the config resource at the given key path.
    """
    node = resources.files(f"{pkgname}.resources.config")
    for key in key_path:
        node = node / key
    return node.read_text()


def ls() -> None:
    """
    Print available config resources, one per line.
    """
    for line in catalog():
        print(line)


def show(key_path: str) -> None:
    """
    Print the text of the config resource at the given slash-separated key path.
    """
    print(extract(key_path.split("/")), end="")


# Private


def _walk(node: Traversable, parts: list[str]) -> list[str]:
    """
    Recursively collect slash-separated paths of files under the given node.
    """
    found = []
    for child in node.iterdir():
        if child.is_dir():
            if child.name != "__pycache__":
                found.extend(_walk(child, [*parts, child.name]))
        elif child.name != "__init__.py":
            found.append("/".join([*parts, child.name]))
    return found
