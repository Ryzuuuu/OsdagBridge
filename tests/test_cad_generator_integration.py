import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from osdagbridge.core.bridge_types.plate_girder.cad_generator import PlateGirderCADGenerator
from osdagbridge.core.bridge_types.plate_girder.dto import BridgeParametersDTO, ShearStudParamsDTO, SectionDimsDTO, ISectionDimsDTO

# Create a mock params object with minimum required fields
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

generator = PlateGirderCADGenerator()
result = generator.generate(params)
print("Keys in result:", result.keys())
print("Piers:", len(result.get("piers", [])))
print("Pier Caps:", len(result.get("pier_caps", [])))
print("Pile Caps:", len(result.get("pile_caps", [])))
print("Piles:", len(result.get("piles", [])))
print("Rebar:", len(result.get("rebar", [])))
