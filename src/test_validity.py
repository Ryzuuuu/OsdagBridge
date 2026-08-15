from OCC.Core.gp import gp_Pnt, gp_Vec
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.BRepCheck import BRepCheck_Analyzer

def test_pier_cap():
    top_width = 3000
    bottom_width = 1200
    depth = 600
    length = 5000
    z_top = 0
    z_bottom = -depth
    center_x = 0
    center_y = 0
    
    half_top = top_width / 2.0
    half_bot = bottom_width / 2.0

    # Old way (Clockwise)
    pts1 = [
        gp_Pnt(center_x - half_top, center_y - length / 2.0, z_top),
        gp_Pnt(center_x + half_top, center_y - length / 2.0, z_top),
        gp_Pnt(center_x + half_bot, center_y - length / 2.0, z_bottom),
        gp_Pnt(center_x - half_bot, center_y - length / 2.0, z_bottom),
    ]
    wire1 = BRepBuilderAPI_MakeWire()
    for i in range(4):
        wire1.Add(BRepBuilderAPI_MakeEdge(pts1[i], pts1[(i+1)%4]).Edge())
    face1 = BRepBuilderAPI_MakeFace(wire1.Wire()).Face()
    solid1 = BRepPrimAPI_MakePrism(face1, gp_Vec(0, length, 0)).Shape()
    analyzer1 = BRepCheck_Analyzer(solid1)
    
    # New way (CCW)
    pts2 = [
        gp_Pnt(center_x - half_top, center_y - length / 2.0, z_top),
        gp_Pnt(center_x - half_bot, center_y - length / 2.0, z_bottom),
        gp_Pnt(center_x + half_bot, center_y - length / 2.0, z_bottom),
        gp_Pnt(center_x + half_top, center_y - length / 2.0, z_top),
    ]
    wire2 = BRepBuilderAPI_MakeWire()
    for i in range(4):
        wire2.Add(BRepBuilderAPI_MakeEdge(pts2[i], pts2[(i+1)%4]).Edge())
    face2 = BRepBuilderAPI_MakeFace(wire2.Wire()).Face()
    solid2 = BRepPrimAPI_MakePrism(face2, gp_Vec(0, length, 0)).Shape()
    analyzer2 = BRepCheck_Analyzer(solid2)
    
    print(f"Old solid valid: {analyzer1.IsValid()}")
    print(f"New solid valid: {analyzer2.IsValid()}")

if __name__ == "__main__":
    test_pier_cap()
