"""
Pile Cap Builder for Bridge Foundation
======================================

Generates parametric 3D CAD geometry for rectangular pile caps using
BRepPrimAPI_MakeBox.

Coordinate System (matches superstructure convention):
    X = Longitudinal (span direction)
    Y = Transverse (deck width direction), centered at Y=0
    Z = Vertical, Z=0 at girder centroid baseline, positive upward

Placement:
    Top of pile cap aligns with bottom of the pier column.
    Z_top = Z_top_pier - pier_height
    Z_bottom = Z_top - pile_cap_depth
"""

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Trsf
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform


# ── Default Parameters ────────────────────────────────────────────────────────

PILE_CAP_LENGTH = 2200.0         # mm — dimension along X (longitudinal)
PILE_CAP_WIDTH = 1200.0          # mm — dimension along Y (transverse)
PILE_CAP_DEPTH = 600.0           # mm — depth (height) along Z


# ── Private Helpers ───────────────────────────────────────────────────────────

def _make_rectangular_cap(length, width, depth, center_x, center_y, z_top):
    """
    Create a rectangular pile cap solid at the specified position.

    The box is centered on center_x and center_y, and extends from
    z_bottom to z_top.

    Args:
        length: Dimension along X (mm).
        width: Dimension along Y (mm).
        depth: Dimension along Z (mm).
        center_x: X coordinate of the cap center.
        center_y: Y coordinate of the cap center.
        z_top: Z coordinate of the top face.

    Returns:
        TopoDS_Shape: Box solid.
    """
    z_bottom = z_top - depth
    half_length = length / 2.0
    half_width = width / 2.0

    # Define the two opposite corners of the box
    p1 = gp_Pnt(center_x - half_length, center_y - half_width, z_bottom)
    p2 = gp_Pnt(center_x + half_length, center_y + half_width, z_top)

    return BRepPrimAPI_MakeBox(p1, p2).Shape()


# ── Public Builder Function ───────────────────────────────────────────────────

def build_pile_cap(
    *,
    length=PILE_CAP_LENGTH,
    width=PILE_CAP_WIDTH,
    depth=PILE_CAP_DEPTH,
    z_top_pile_cap,
    x_positions,
    y_position=0.0,
):
    """
    Build rectangular pile caps at specified longitudinal positions.

    Args:
        length: Pile cap length along X-axis (mm). Default 2200.
        width: Pile cap width along Y-axis (mm). Default 1200.
        depth: Pile cap depth/height (mm). Default 600.
        z_top_pile_cap: Z coordinate of the top of the pile cap
                        (= bottom of pier column).
        x_positions: List of X coordinates where pile caps are placed.
        y_position: Y coordinate of pile cap center (transverse). Default 0.0.

    Returns:
        dict: {"pile_caps": [TopoDS_Shape, ...]} — one box solid per x_position.
    """
    pile_caps = []

    for x in x_positions:
        cap = _make_rectangular_cap(
            length=length,
            width=width,
            depth=depth,
            center_x=x,
            center_y=y_position,
            z_top=z_top_pile_cap,
        )
        pile_caps.append(cap)

    return {"pile_caps": pile_caps}
