"""
Pier Cap Builder for Bridge Substructure
=========================================

Generates parametric 3D CAD geometry for hammerhead/trapezoidal pier caps
using face extrusion (BRepBuilderAPI_MakeFace + BRepPrimAPI_MakePrism).

The cross-section is trapezoidal (wider at top, narrower at bottom) when
viewed from the side (X–Z plane). The cap extends along the Y-axis (transverse)
for the full deck width.

Coordinate System (matches superstructure convention):
    X = Longitudinal (span direction)
    Y = Transverse (deck width direction), centered at Y=0
    Z = Vertical, Z=0 at girder centroid baseline, positive upward

Placement:
    Top of pier cap aligns with bottom of girder bottom flanges.
    Z_top = -(girder_depth/2 + bottom_flange_thickness)
    Z_bottom = Z_top - pier_cap_depth
"""

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Trsf
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.BRepBuilderAPI import (
    BRepBuilderAPI_MakeEdge,
    BRepBuilderAPI_MakeWire,
    BRepBuilderAPI_MakeFace,
    BRepBuilderAPI_Transform,
)


# ── Default Parameters ────────────────────────────────────────────────────────

PIER_CAP_TOP_WIDTH = 3000.0      # mm — top width of trapezoidal cross-section
PIER_CAP_BOTTOM_WIDTH = 1200.0   # mm — bottom width of trapezoidal cross-section
PIER_CAP_DEPTH = 600.0           # mm — depth (height) of pier cap


# ── Private Helpers ───────────────────────────────────────────────────────────

def _make_edge(p1, p2):
    """Create a TopoDS_Edge between two gp_Pnt points."""
    return BRepBuilderAPI_MakeEdge(p1, p2).Edge()


def _make_wire_from_points(points):
    """Create a closed wire from a list of gp_Pnt points."""
    wire_maker = BRepBuilderAPI_MakeWire()
    for i in range(len(points)):
        p_start = points[i]
        p_end = points[(i + 1) % len(points)]
        wire_maker.Add(_make_edge(p_start, p_end))
    return wire_maker.Wire()


def _make_trapezoidal_cap(top_width, bottom_width, depth, length, center_x, center_y, z_top):
    """
    Create a trapezoidal pier cap solid at the specified position.

    The trapezoidal cross-section is in the X–Z plane:
        - Top face: width = top_width, centered on center_x
        - Bottom face: width = bottom_width, centered on center_x
        - Depth: from z_top downward by 'depth'

    The cap is extruded along the Y-axis for 'length', centered on center_y.

    Args:
        top_width: Width of the cap at the top (mm).
        bottom_width: Width of the cap at the bottom (mm).
        depth: Depth (height) of the cap (mm).
        length: Extent along Y-axis (transverse, = total_deck_width) (mm).
        center_x: X coordinate of the cap center.
        center_y: Y coordinate of the cap center.
        z_top: Z coordinate of the top face.

    Returns:
        TopoDS_Shape: Trapezoidal prism solid.
    """
    z_bottom = z_top - depth
    half_top = top_width / 2.0
    half_bot = bottom_width / 2.0

    # Define trapezoidal cross-section in X–Z plane at Y = center_y - length/2
    # Points go counter-clockwise when viewed from -Y direction (looking at XZ plane from outside)
    pts = [
        gp_Pnt(center_x - half_top, center_y - length / 2.0, z_top),
        gp_Pnt(center_x - half_bot, center_y - length / 2.0, z_bottom),
        gp_Pnt(center_x + half_bot, center_y - length / 2.0, z_bottom),
        gp_Pnt(center_x + half_top, center_y - length / 2.0, z_top),
    ]



    wire = _make_wire_from_points(pts)
    face = BRepBuilderAPI_MakeFace(wire).Face()

    # Extrude along +Y for the full length
    extrude_vec = gp_Vec(0, length, 0)
    return BRepPrimAPI_MakePrism(face, extrude_vec).Shape()


# ── Public Builder Function ───────────────────────────────────────────────────

def build_pier_cap(
    *,
    top_width=PIER_CAP_TOP_WIDTH,
    bottom_width=PIER_CAP_BOTTOM_WIDTH,
    depth=PIER_CAP_DEPTH,
    length,
    z_top_pier_cap,
    x_positions,
    y_position=0.0,
):
    """
    Build trapezoidal pier caps at specified longitudinal positions.

    Args:
        top_width: Top width of trapezoidal cross-section (mm). Default 3000.
        bottom_width: Bottom width of trapezoidal cross-section (mm). Default 1200.
        depth: Pier cap depth/height (mm). Default 600.
        length: Pier cap length along Y-axis (mm). Auto-derived from total_deck_width.
        z_top_pier_cap: Z coordinate of the top of the pier cap
                        (= bottom of girder bottom flange).
        x_positions: List of X coordinates where pier caps are placed.
        y_position: Y coordinate of pier cap center (transverse). Default 0.0.

    Returns:
        dict: {"pier_caps": [TopoDS_Shape, ...]} — one trapezoidal solid per x_position.
    """
    pier_caps = []

    for x in x_positions:
        cap = _make_trapezoidal_cap(
            top_width=top_width,
            bottom_width=bottom_width,
            depth=depth,
            length=length,
            center_x=x,
            center_y=y_position,
            z_top=z_top_pier_cap,
        )
        pier_caps.append(cap)

    return {"pier_caps": pier_caps}
