from collections.abc import Iterator, Sequence
from contextlib import ExitStack, contextmanager
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path

from uwtools.api.config import YAMLConfig, compose_to_dict

from rheos.util import pkgname


def catalog() -> list[str]:
    """
    Catalog config resources as slash-separated paths relative to the config-resources root.
    """
    return sorted(_walk(_root(), []))


def compose(configs: Sequence[str | Path], *, realize: bool = False) -> YAMLConfig:
    """
    Return the composition of the given configs.
    """
    with _paths(configs) as paths:
        return YAMLConfig(compose_to_dict(paths, realize=realize))


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
def _paths(configs: Sequence[str | Path]) -> Iterator[list[Path]]:
    """
    Yield filesystem paths for the given configs, preferring existing files over config resources.
    """
    with ExitStack() as stack:
        yield [
            Path(config)
            if Path(config).is_file()
            else stack.enter_context(resources.as_file(_node(Path(config).as_posix())))
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
