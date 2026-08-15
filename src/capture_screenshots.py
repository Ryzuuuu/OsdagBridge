import sys
import os
import time

sys.path.insert(0, r"C:\Users\neela\OneDrive\Desktop\OsdagBridge\src")

from PySide6.QtWidgets import QApplication
from osdagbridge.desktop.ui.cad_3d import CAD3DWindow

def run():
    app = QApplication(sys.argv)
    
    cad_widget = CAD3DWindow()
    cad_widget.show()

    # Wait for UI to initialize
    QApplication.processEvents()

    # Let's bypass UI clicks and just invoke the CAD 3D renderer with default parameters
    from osdagbridge.core.bridge_types.plate_girder.dto import BridgeParametersDTO, ShearStudParamsDTO, SectionDimsDTO, ISectionDimsDTO
    from osdagbridge.core.bridge_types.plate_girder.cad_generator import PlateGirderCADGenerator
    
    params = BridgeParametersDTO(
        steel_grade="E250 (Fe 410W)A",
        concrete_grade="M30",
        span_length_L=20000,
        girder_section_d=1200,
        girder_section_bf=400,
        girder_section_bf_b=400,
        girder_section_tf=20,
        girder_section_tf_b=20,
        girder_section_tw=10,
        num_girders=3,
        girder_spacing=2500,
        carriageway_width=7500,
        deck_thickness=200,
        footpath_config="NONE",
        footpath_width=1000,
        railing_width=200,
        barrier_type="Rigid",
        crash_barrier_subtype="IRC-5R",
        enable_median=False,
        median_type="",
        rail_count=3,
        railing_type="rcc",
        include_intermediate_stiffeners=False,
        intermediate_stiffener_spacing=2000,
        intermediate_stiffener_thickness=20,
        intermediate_stiffener_outstand=None,
        num_end_stiffener_pairs=4,
        end_stiffener_thickness=30,
        end_stiffener_outstand=None,
        include_longitudinal_stiffeners=False,
        num_longitudinal_stiffeners=2,
        longitudinal_stiffener_thickness=20,
        longitudinal_stiffener_outstand=None,
        cross_bracing_spacing=5000,
        bracing_type="X",
        x_bracket_option="BOTH",
        k_top_bracket=True,
        diagonal_section_type="ANGLE",
        diagonal_thickness=5,
        top_chord_section_type="ANGLE",
        top_chord_thickness=5,
        bottom_chord_section_type="ANGLE",
        bottom_chord_thickness=5,
        end_diaphragm_type="Cross Bracing",
        end_diaphragm_spacing=100,
        end_diaphragm_bracing_type="K",
        end_diaphragm_diagonal_section_type="ANGLE",
        end_diaphragm_diagonal_thickness=5,
        end_diaphragm_top_chord_section_type="ANGLE",
        end_diaphragm_top_chord_thickness=5,
        end_diaphragm_bottom_chord_section_type="ANGLE",
        end_diaphragm_bottom_chord_thickness=5,
        end_diaphragm_section="I_SECTION",
        skew_angle=0,
        shear_stud_params=ShearStudParamsDTO(
            base_diameter=20, top_diameter=30, base_height=10, top_height=100, 
            num_per_section=2, transverse_spacing=100, pitch=300
        ),
        diagonal_section_dims=SectionDimsDTO(leg_h=100, leg_w=100, connection_type="LONGER_LEG"),
        top_chord_section_dims=SectionDimsDTO(leg_h=100, leg_w=100, connection_type="LONGER_LEG"),
        bottom_chord_section_dims=SectionDimsDTO(leg_h=100, leg_w=100, connection_type="LONGER_LEG"),
        end_diaphragm_diagonal_section_dims=SectionDimsDTO(leg_h=100, leg_w=100, connection_type="LONGER_LEG"),
        end_diaphragm_top_chord_section_dims=SectionDimsDTO(leg_h=100, leg_w=100, connection_type="LONGER_LEG"),
        end_diaphragm_bottom_chord_section_dims=SectionDimsDTO(leg_h=100, leg_w=100, connection_type="LONGER_LEG"),
        end_diaphragm_dims=ISectionDimsDTO(depth=100, flange_width=100, web_thickness=10, flange_thickness=10)
    )
    gen = PlateGirderCADGenerator()
    cad_data = gen.generate(params)
    print("DEBUG: CAD data generated.")
    
    # We want to render ONLY the pier cap to isolate it for the screenshot
    cad_widget.generator = gen
    
    display = cad_widget.viewer._display
    
    # We will override the generated shapes in the canvas to only be the pier caps
    display.EraseAll()
    
    from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
    CONCRETE_COLOR = Quantity_Color(150/255, 150/255, 150/255, Quantity_TOC_RGB)
    
    print("DEBUG: Registering ONLY pier_caps")
    display = cad_widget.viewer._display
    for pc in cad_data.get("pier_caps", []):
        ais = display.DisplayShape(pc, color=CONCRETE_COLOR, update=False)
        ais = ais[0] if isinstance(ais, list) else ais
        # Make it opaque so taper is even more visible, or transparent if you want
        cad_widget.viewer.context.SetTransparency(ais, 0.0, False)
    
    QApplication.processEvents()
    time.sleep(2)

    # Zoom to pier cap, look along Y-axis to see the X-Z plane taper
    print("DEBUG: Capturing screenshot 1 (Pier Cap Taper Isolated)...")
    display.View_Front() # look along Y axis (front view is usually +Y or -Y)
    display.FitAll()
    display.ZoomFactor(2.0)
    
    QApplication.processEvents()
    display.View.Dump(r"C:\Users\neela\OneDrive\Desktop\OsdagBridge\src\pier_cap_isolated.png")
    
    print("DEBUG: Screenshots saved.")
    app.quit()

if __name__ == "__main__":
    run()
