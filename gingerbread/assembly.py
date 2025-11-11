from build123d import *
from ocp_vscode import *

from . import base, front
from .spec import *

# Base stays at origin
base_part = base.part.part

origin = base.origin_corner

front_part = front.part.part.moved(Location(origin))
back_part = front_part.moved(Rotation(Z=180))

assembly = Compound(label="assembly", children=[base_part, front_part, back_part])

push_object(assembly, name="Assembly")
