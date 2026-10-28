from importlib import resources
from importlib.resources.abc import Traversable

from rheos.util import pkgname


def compose() -> None:
    """
    Compose a config.
    """
    print("rheos.api.config.compose() called")


def extract(key_path: list[str]) -> str:
    """
    Return the text of the config resource at the given key path.
    """
    node = resources.files(f"{pkgname}.resources.config")
    for key in key_path:
        node = node / key
    return node.read_text()


def extract_to_stdout(key_path: str) -> None:
    """
    Print the text of the config resource at the given slash-separated key path.
    """
    print(extract(key_path.split("/")), end="")


def ls() -> list[str]:
    """
    List available config resources as slash-separated paths relative to the config resources root.
    """
    return sorted(_walk(resources.files(f"{pkgname}.resources.config"), []))


def ls_to_stdout() -> None:
    """
    Print available config resources, one per line.
    """
    for line in ls():
        print(line)


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
