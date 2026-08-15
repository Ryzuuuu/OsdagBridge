# OsdagBridge: Substructure 3D CAD & IFC Integration Report

## 1. Methodology

The substructure modeling for OsdagBridge utilizes a procedural, parametric geometry generation approach powered by `pythonOCC` (OpenCASCADE). The architecture is divided into five modular builders, each responsible for specific reinforced concrete components:

*   **Piers & Piles (`pier`, `pile`)**: Utilized `BRepPrimAPI_MakeCylinder` for generating circular profiles extruded vertically.
*   **Pile Caps (`pile_cap`)**: Generated via `BRepPrimAPI_MakeBox` to produce solid rectangular foundations.
*   **Pier Caps (`pier_cap`)**: Modeled as complex tapered trapezoidal prisms. The cross-sectional face was generated in the X-Z plane using `BRepBuilderAPI_MakeWire` and `BRepBuilderAPI_MakeFace`, then extruded along the transverse Y-axis via `BRepPrimAPI_MakePrism`.
*   **Reinforcement (`reinforcement`)**: Designed 3D rebar cages encompassing both longitudinal/vertical main bars and transverse ties (rings) by utilizing thin cylindrical sweeps and torus geometries (`BRepPrimAPI_MakeTorus`).

These builders are orchestrated by `cad_generator.py`, which acts as the topological assembly engine. It evaluates the global parameters (deck width, girder depth, span length) to compute relative 3D coordinate origins (`gp_Pnt`) and translations (`gp_Trsf`). The aggregated shape data is organized into a semantic dictionary and passed directly to the presentation layer in `cad_3d.py`. 

The `cad_3d.py` UI script iterates over this data, encapsulating the raw `TopoDS_Shape` objects into `AIS_Shape` representations. It binds them to the PySide6 viewer context, managing colors (`RCC_COLOR`, `REBAR_COLOR`), selectable flags, and alpha transparencies.

## 2. IFC4 BIM Integration

Interoperability is achieved by porting the `pythonOCC` generated shapes into the Industry Foundation Classes (IFC4) schema using `IfcOpenShell`. 

**Semantic Mapping & Spatial Hierarchy**
To distinguish substructure elements from the steel superstructure, a dedicated `IfcBuildingStorey` titled `"Substructure"` was created beneath the root `IfcBuilding`. Components were strictly typed to their semantic IFC equivalents:
*   **Pier Caps** -> `IfcBeam` (Horizontal load-bearing)
*   **Piers** -> `IfcColumn` (Vertical load-bearing)
*   **Pile Caps** -> `IfcFooting` (Foundation block)
*   **Piles** -> `IfcPile` (Deep foundation)
*   **Rebar** -> `IfcReinforcingBar`

**Placement Logic**
The exporter maps the OpenCASCADE geometries to `IfcFacetedBrep` representations. Local placements (`IfcLocalPlacement`) are applied hierarchically. Substructure components are anchored relative to the `"Substructure"` storey placement, ensuring that when imported into external BIM viewers (e.g., Revit, BIMvision), the physical locations align perfectly with the superstructure without Z-axis overlap or floating geometries.

## 3. Challenges & Resolutions

### Environment Setup & Dependency Conflicts
Early development was heavily blocked by environment instability inside the local `conda` environment. 
*   **DLL Corruption**: `PySide6` and `shiboken6` modules suffered from underlying ABI mismatch errors causing hard crashes upon GUI initialization. This required forcefully isolating Qt bindings and utilizing the `mamba` solver to strictly resolve compatible Python 3.10 binaries.
*   **`osdag_core` Missing Modules**: The standard `osdag` pip/conda distributions were severely out-of-date and lacked the core DTO and CLI structures required by `OsdagBridge`. The solution involved pulling the latest codebase directly from the upstream developer branch of the Osdag repository and manually linking it into the Python path.

### OpenCASCADE Rendering Quirks (`cad_3d.py`)
Two subtle but critical rendering bugs occurred in the interactive 3D viewport, despite mathematically correct underlying geometry:
*   **The Transparency & Rebar Bug**: Concrete elements rendered as fully opaque white, entirely obscuring the internal rebar. Our initial attempt to pass `transparency` directly into the `kwargs` of `display.DisplayShape(shp, **kwargs)` was unreliable and silently ignored across different pythonOCC builds.
    *   **Fix**: We reverted to calling `ais.SetTransparency(float(transparency))` directly on the returned `AIS_Shape` object *after* `DisplayShape()` creates it, followed immediately by `context.RecomputePrsOnly(ais, False)` to force a redraw. This reliably applies the transparency and makes the concrete translucent, exposing the rebar inside.
*   **The Pier Cap Taper Bug**: The trapezoidal pier cap rendered as a plain rectangular bounding box. This occurred because the X-Z points were ordered in a clockwise direction, creating a face normal pointing against the intended extrusion vector (`-Y`). OpenCASCADE reacts to this inverted topological extrusion by defaulting to a bounding-box visual artifact. 
    *   **Fix**: The `gp_Pnt` generation was rewritten to enforce a strict counter-clockwise winding order, ensuring a valid topology and restoring the visible taper.

## 4. References
1. **pythonOCC Documentation**: https://dev.opencascade.org/doc/overview/html/index.html (Python bindings for OpenCASCADE CAD kernel)
2. **IfcOpenShell Academy**: https://blenderbim.org/docs-python/ (Schema reference and procedural IFC generation)
3. **Osdag Source Repository**: https://github.com/osdag-admin/Osdag (Core modules and structural standards)
4. **OsdagBridge Repository**: https://github.com/osdag-admin/OsdagBridge (Bridge extensions)
