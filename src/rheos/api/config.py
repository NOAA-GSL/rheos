import builtins
from importlib import resources
from importlib.resources.abc import Traversable

from rheos.util import pkgname


def compose() -> None:
    """
    Compose a config.
    """
    print("rheos.api.config.compose() called")  # noqa: T201


def extract() -> None:
    """
    Extract a config.
    """
    print("rheos.api.config.extract() called")  # noqa: T201


def list() -> builtins.list[str]:  # noqa: A001
    """
    List available config resources as dotted strings relative to the config resources root.
    """
    return sorted(_walk(resources.files(f"{pkgname}.resources.config"), []))


def list_to_log() -> None:
    """
    Print available config resources, one per line.
    """
    for line in list():
        print(line)  # noqa: T201


# Private


def _walk(node: Traversable, parts: builtins.list[str]) -> builtins.list[str]:
    """
    Recursively collect dotted names of files under the given node.
    """
    found = []
    for child in node.iterdir():
        if child.is_dir():
            if child.name != "__pycache__":
                found.extend(_walk(child, [*parts, child.name]))
        elif child.name != "__init__.py":
            found.append(".".join([*parts, child.name]))
    return found
