"""Display the D-shaft knob model in OCP CAD Viewer."""

from ocp_vscode import push_object, show_objects

from main import knob_part

push_object(knob_part, name="D-Shaft Knob")
show_objects()
