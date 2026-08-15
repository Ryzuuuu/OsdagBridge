import ifcopenshell
import ifcopenshell.geom
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.Bnd import Bnd_Box
import math

def get_bounding_box(shape):
    bbox = Bnd_Box()
    brepbndlib.Add(shape, bbox)
    
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    return xmin, ymin, zmin, xmax, ymax, zmax

def print_bbox(file_path):
    print(f"Loading {file_path}...")
    f = ifcopenshell.open(file_path)
    
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)
    
    for element_type in ['IfcColumn', 'IfcBeam', 'IfcFooting', 'IfcPile']:
        elements = f.by_type(element_type)
        if not elements:
            continue
            
        print(f"\n--- {element_type} ({len(elements)} items) ---")
        for i, el in enumerate(elements):
            name = el.Name if el.Name else "Unnamed"
            if element_type == 'IfcBeam' and 'Pier Cap' not in name:
                continue
                
            try:
                shape = ifcopenshell.geom.create_shape(settings, el)
                occ_shape = shape.geometry
                
                xmin, ymin, zmin, xmax, ymax, zmax = get_bounding_box(occ_shape)
                
                lx = xmax - xmin
                ly = ymax - ymin
                lz = zmax - zmin
                
                print(f"[{i}] {name}:")
                print(f"    Min (X, Y, Z): ({xmin:.2f}, {ymin:.2f}, {zmin:.2f})")
                print(f"    Max (X, Y, Z): ({xmax:.2f}, {ymax:.2f}, {zmax:.2f})")
                print(f"    Dimensions (Lx, Ly, Lz): {lx:.2f} x {ly:.2f} x {lz:.2f}")
                
            except Exception as e:
                print(f"[{i}] {name}: Could not compute bounding box ({e})")

if __name__ == "__main__":
    print_bbox("real_design.ifc")
