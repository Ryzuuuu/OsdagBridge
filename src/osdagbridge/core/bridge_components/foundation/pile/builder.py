"""
Pile Builder for Bridge Foundation
==================================

Generates parametric 3D CAD geometry for foundation piles.
Creates a grid of circular cylindrical piles under the pile cap.

Coordinate System (matches superstructure convention):
    X = Longitudinal (span direction)
    Y = Transverse (deck width direction), centered at Y=0
    Z = Vertical, Z=0 at girder centroid baseline, positive upward

Placement:
    Top of piles aligns with bottom of the pile cap.
    Z_top = Z_top_pile_cap - pile_cap_depth
    Z_bottom = Z_top - pile_length
"""

from OCC.Core.gp import gp_Pnt, gp_Ax2, gp_Dir
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder


# ── Default Parameters ────────────────────────────────────────────────────────

PILE_DIAMETER = 400.0            # mm
PILE_LENGTH = 5000.0             # mm
PILE_GRID_NX = 2                 # Number of piles in X direction
PILE_GRID_NY = 2                 # Number of piles in Y direction
PILE_SPACING = 600.0             # mm (center-to-center spacing)


# ── Private Helpers ───────────────────────────────────────────────────────────

def _make_circular_pile(diameter, length, center_x, center_y, z_bottom):
    """
    Create a single cylindrical pile at the specified position.

    Args:
        diameter: Pile diameter (mm).
        length: Pile length (depth) (mm).
        center_x: X coordinate of pile center.
        center_y: Y coordinate of pile center.
        z_bottom: Z coordinate of pile tip (bottom).

    Returns:
        TopoDS_Shape: Cylinder solid.
    """
    radius = diameter / 2.0
    axis = gp_Ax2(gp_Pnt(center_x, center_y, z_bottom), gp_Dir(0, 0, 1))
    return BRepPrimAPI_MakeCylinder(axis, radius, length).Shape()


# ── Public Builder Function ───────────────────────────────────────────────────

def build_piles(
    *,
    num_x=PILE_GRID_NX,
    num_y=PILE_GRID_NY,
    diameter=PILE_DIAMETER,
    length=PILE_LENGTH,
    spacing=PILE_SPACING,
    z_top_piles,
    x_positions,
    y_position=0.0,
):
    """
    Build foundation piles in a grid at specified longitudinal positions.

    Args:
        num_x: Number of piles along the longitudinal direction (X).
        num_y: Number of piles along the transverse direction (Y).
        diameter: Pile diameter (mm).
        length: Pile length (mm).
        spacing: Center-to-center spacing between piles (mm).
        z_top_piles: Z coordinate of the top of the piles (bottom of pile cap).
        x_positions: List of X coordinates for the center of the pile groups.
        y_position: Y coordinate for the center of the pile groups. Default 0.0.

    Returns:
        dict: {"piles": [TopoDS_Shape, ...]} — list of all pile cylinders.
    """
    piles = []
    z_bottom = z_top_piles - length

    # Calculate offsets to center the grid around the group center
    total_x_width = (num_x - 1) * spacing
    total_y_width = (num_y - 1) * spacing

    for x_center in x_positions:
        start_x = x_center - (total_x_width / 2.0)
        start_y = y_position - (total_y_width / 2.0)

        for i in range(num_x):
            for j in range(num_y):
                px = start_x + (i * spacing)
                py = start_y + (j * spacing)

                pile = _make_circular_pile(
                    diameter=diameter,
                    length=length,
                    center_x=px,
                    center_y=py,
                    z_bottom=z_bottom,
                )
                piles.append(pile)

    return {"piles": piles}
