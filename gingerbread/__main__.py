from build123d import *
from ocp_vscode import *

from . import (
    assembly,  # noqa: F401
    base,  # noqa: F401
    front,  # noqa: F401
)
from .spec import *

show_objects(
    show_sketch_local=False,
)
