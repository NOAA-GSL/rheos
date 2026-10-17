import json
from importlib import resources
from pathlib import Path
from typing import cast

pkgname = __name__.split(".", maxsplit=1)[0]


def resource(relpath: str | Path) -> str:
    return resource_path(relpath).read_text()


def resource_path(relpath: str | Path) -> Path:
    return cast(
        Path,
        resources.files(f"{pkgname}.resources").joinpath(str(relpath))
    )


def version() -> str:
    info = json.loads(resource("info.json"))
    return "version %s" % info["version"]
