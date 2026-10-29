from collections.abc import Iterator
from contextlib import ExitStack, contextmanager
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path

from uwtools.api.config import compose as uw_compose
from uwtools.api.config import compose_to_dict as uw_compose_to_dict
from uwtools.config.formats.base import Config

from rheos.util import pkgname


def cat(key_path: str) -> None:
    """
    Print the text of the config resource at the given slash-separated key path.
    """
    print(read(key_path.split("/")), end="")


def catalog() -> list[str]:
    """
    Catalog available config resources as slash-separated paths relative to the config resources
    root.
    """
    return sorted(_walk(_root(), []))


def compose(configs: list[str], *, realize: bool = False) -> Config:
    """
    Compose the given configs, writing the result to stdout.

    Each config is a filesystem path, if such a file exists, or else a slash-separated key path to a
    config resource.
    """
    with _paths(configs) as paths:
        return uw_compose(paths, realize=realize)


def compose_to_dict(configs: list[str], *, realize: bool = False) -> dict:
    """
    Compose the given configs and return the result as a dict.

    Each config is a filesystem path, if such a file exists, or else a slash-separated key path to a
    config resource.
    """
    with _paths(configs) as paths:
        return uw_compose_to_dict(paths, realize=realize)


def ls() -> None:
    """
    Print available config resources, one per line.
    """
    for line in catalog():
        print(line)


def read(key_path: list[str]) -> str:
    """
    Return the text of the config resource at the given key path.
    """
    return _node("/".join(key_path)).read_text()


# Private


def _node(key_path: str) -> Traversable:
    """
    Return the config resource at the given slash-separated key path.
    """
    node = _root()
    for key in key_path.split("/"):
        node = node / key
    return node


@contextmanager
def _paths(configs: list[str]) -> Iterator[list[Path]]:
    """
    Yield filesystem paths for the given configs, preferring existing files over config resources.
    """
    with ExitStack() as stack:
        yield [
            Path(config)
            if Path(config).is_file()
            else stack.enter_context(resources.as_file(_node(config)))
            for config in configs
        ]


def _root() -> Traversable:
    """
    Return the root of the config resources.
    """
    return resources.files(f"{pkgname}.resources.config")


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
