"""
Pier Builder for Bridge Substructure
=====================================

Generates parametric 3D CAD geometry for circular bridge piers using
BRepPrimAPI_MakeCylinder. Follows the same procedural pattern as
existing superstructure builders (keyword-only args, dict return).

Coordinate System (matches superstructure convention):
    X = Longitudinal (span direction)
    Y = Transverse (deck width direction), centered at Y=0
    Z = Vertical, Z=0 at girder centroid baseline, positive upward

Placement:
    Top of pier connects to bottom of pier cap.
    Z_top_pier = -(girder_depth/2 + bottom_flange_thickness + pier_cap_depth)
    Z_bottom_pier = Z_top_pier - pier_height
"""

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Trsf, gp_Ax2, gp_Dir
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform


# ── Default Parameters ────────────────────────────────────────────────────────

PIER_DIAMETER = 800.0        # mm — circular column diameter
PIER_HEIGHT = 3000.0         # mm — pier height


# ── Private Helpers ───────────────────────────────────────────────────────────

def _translate(shape, dx=0.0, dy=0.0, dz=0.0):
    """Translate a TopoDS_Shape by (dx, dy, dz)."""
    trsf = gp_Trsf()
    trsf.SetTranslation(gp_Vec(dx, dy, dz))
    return BRepBuilderAPI_Transform(shape, trsf, True).Shape()


def _make_circular_column(diameter, height, center_x, center_y, z_bottom):
    """
    Create a circular cylinder (pier column) at the specified position.

    The cylinder axis is vertical (Z-up), with its base at z_bottom.

    Args:
        diameter: Column diameter in mm.
        height: Column height in mm.
        center_x: X coordinate of column center.
        center_y: Y coordinate of column center.
        z_bottom: Z coordinate of column base (bottom).

    Returns:
        TopoDS_Shape: Cylinder solid.
    """
    radius = diameter / 2.0
    # gp_Ax2 defines the cylinder axis: origin at base center, direction = +Z
    axis = gp_Ax2(gp_Pnt(center_x, center_y, z_bottom), gp_Dir(0, 0, 1))
    return BRepPrimAPI_MakeCylinder(axis, radius, height).Shape()


# ── Public Builder Function ───────────────────────────────────────────────────

def build_pier(
    *,
    diameter=PIER_DIAMETER,
    height=PIER_HEIGHT,
    z_top_pier,
    x_positions,
    y_position=0.0,
):
    """
    Build circular pier columns at specified longitudinal positions.

    Args:
        diameter: Pier column diameter (mm). Default 800.
        height: Pier column height (mm). Default 3000.
        z_top_pier: Z coordinate of the top of the pier (connects to pier cap bottom).
        x_positions: List of X coordinates where piers are placed (e.g. [0, span_length]).
        y_position: Y coordinate of pier center (transverse). Default 0.0 (centered).

    Returns:
        dict: {"piers": [TopoDS_Shape, ...]} — one cylinder per x_position.
    """
    z_bottom = z_top_pier - height
    piers = []

    for x in x_positions:
        pier = _make_circular_column(
            diameter=diameter,
            height=height,
            center_x=x,
            center_y=y_position,
            z_bottom=z_bottom,
        )
        piers.append(pier)

    return {"piers": piers}
