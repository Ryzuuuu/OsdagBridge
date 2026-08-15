"""
Substructure Builder Test Script
================================
Tests each builder incrementally. Run with:
    conda activate osdagbridge-env
    cd src
    python ../tests/test_substructure_builders.py --step 1
"""
import sys
import os

# Ensure src is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib


def get_bounding_box(shape):
    """Return (xmin, ymin, zmin, xmax, ymax, zmax) for a shape."""
    box = Bnd_Box()
    brepbndlib.Add(shape, box)
    return box.Get()


def test_pier():
    print("=" * 60)
    print("STEP 1: Testing build_pier()")
    print("=" * 60)

    from osdagbridge.core.bridge_components.sub_structure.pier.builder import build_pier

    girder_d = 1200.0
    tf_b = 20.0
    pier_cap_depth = 600.0
    z_top_pier = -(girder_d / 2 + tf_b + pier_cap_depth)
    span_length = 20000.0

    result = build_pier(
        diameter=800,
        height=3000,
        z_top_pier=z_top_pier,
        x_positions=[0.0, span_length],
        y_position=0.0,
    )

    piers = result["piers"]
    print(f"  Shape count: {len(piers)} (expected 2)")
    assert len(piers) == 2, f"Expected 2 piers, got {len(piers)}"

    for i, pier in enumerate(piers):
        bb = get_bounding_box(pier)
        print(f"  Pier {i} bounding box: xmin={bb[0]:.1f} ymin={bb[1]:.1f} zmin={bb[2]:.1f}"
              f" xmax={bb[3]:.1f} ymax={bb[4]:.1f} zmax={bb[5]:.1f}")
        actual_height = bb[5] - bb[2]
        assert abs(actual_height - 3000.0) < 1.0, f"Height mismatch: {actual_height}"
        actual_diameter_x = bb[3] - bb[0]
        assert abs(actual_diameter_x - 800.0) < 1.0, f"Diameter mismatch X: {actual_diameter_x}"

    print("  STEP 1 PASSED\n")


def test_pier_cap():
    print("=" * 60)
    print("STEP 2: Testing build_pier_cap()")
    print("=" * 60)

    from osdagbridge.core.bridge_components.sub_structure.pier_cap.builder import build_pier_cap

    girder_d = 1200.0
    tf_b = 20.0
    z_bottom_flange = -(girder_d / 2 + tf_b)
    span_length = 20000.0
    total_deck_width = 8000.0

    result = build_pier_cap(
        top_width=3000,
        bottom_width=1200,
        depth=600,
        length=total_deck_width,
        z_top_pier_cap=z_bottom_flange,
        x_positions=[0.0, span_length],
        y_position=0.0,
    )

    caps = result["pier_caps"]
    print(f"  Shape count: {len(caps)} (expected 2)")
    assert len(caps) == 2, f"Expected 2 pier caps, got {len(caps)}"

    for i, cap in enumerate(caps):
        bb = get_bounding_box(cap)
        print(f"  Pier cap {i} bounding box: xmin={bb[0]:.1f} ymin={bb[1]:.1f} zmin={bb[2]:.1f}"
              f" xmax={bb[3]:.1f} ymax={bb[4]:.1f} zmax={bb[5]:.1f}")
        actual_depth = bb[5] - bb[2]
        assert abs(actual_depth - 600.0) < 1.0, f"Depth mismatch: {actual_depth}"
        actual_length = bb[4] - bb[1]
        assert abs(actual_length - total_deck_width) < 1.0, f"Length mismatch: {actual_length}"

    print("  STEP 2 PASSED\n")


def test_pile_cap():
    print("=" * 60)
    print("STEP 3: Testing build_pile_cap()")
    print("=" * 60)

    from osdagbridge.core.bridge_components.foundation.pile_cap.builder import build_pile_cap

    girder_d = 1200.0
    tf_b = 20.0
    pier_cap_depth = 600.0
    pier_height = 3000.0
    z_top_pile_cap = -(girder_d / 2 + tf_b + pier_cap_depth + pier_height)
    span_length = 20000.0

    result = build_pile_cap(
        length=2200,
        width=1200,
        depth=600,
        z_top_pile_cap=z_top_pile_cap,
        x_positions=[0.0, span_length],
        y_position=0.0,
    )

    caps = result["pile_caps"]
    print(f"  Shape count: {len(caps)} (expected 2)")
    assert len(caps) == 2, f"Expected 2 pile caps, got {len(caps)}"

    for i, cap in enumerate(caps):
        bb = get_bounding_box(cap)
        print(f"  Pile cap {i} bounding box: xmin={bb[0]:.1f} ymin={bb[1]:.1f} zmin={bb[2]:.1f}"
              f" xmax={bb[3]:.1f} ymax={bb[4]:.1f} zmax={bb[5]:.1f}")
        actual_depth = bb[5] - bb[2]
        assert abs(actual_depth - 600.0) < 1.0, f"Depth mismatch: {actual_depth}"

    print("  STEP 3 PASSED\n")


def test_piles():
    print("=" * 60)
    print("STEP 4: Testing build_piles()")
    print("=" * 60)

    from osdagbridge.core.bridge_components.foundation.pile.builder import build_piles

    girder_d = 1200.0
    tf_b = 20.0
    pier_cap_depth = 600.0
    pier_height = 3000.0
    pile_cap_depth = 600.0
    z_bottom_pile_cap = -(girder_d / 2 + tf_b + pier_cap_depth + pier_height + pile_cap_depth)
    span_length = 20000.0

    result = build_piles(
        num_x=2,
        num_y=2,
        diameter=400,
        length=5000,
        spacing=600,
        z_top_piles=z_bottom_pile_cap,
        x_positions=[0.0, span_length],
        y_position=0.0,
    )

    piles = result["piles"]
    print(f"  Shape count: {len(piles)} (expected 8)")
    assert len(piles) == 8, f"Expected 8 piles, got {len(piles)}"

    for i, pile in enumerate(piles):
        bb = get_bounding_box(pile)
        actual_length = bb[5] - bb[2]
        assert abs(actual_length - 5000.0) < 1.0, f"Pile {i} length mismatch: {actual_length}"

    print("  STEP 4 PASSED\n")


def test_reinforcement():
    print("=" * 60)
    print("STEP 5: Testing build_reinforcement()")
    print("=" * 60)

    from osdagbridge.core.bridge_components.sub_structure.pier.builder import build_pier
    from osdagbridge.core.bridge_components.sub_structure.reinforcement.builder import build_reinforcement

    z_top_pier = -1220.0
    pier_result = build_pier(
        diameter=800, height=3000, z_top_pier=z_top_pier,
        x_positions=[0.0], y_position=0.0
    )
    pier_shape = pier_result["piers"][0]

    rebar = build_reinforcement(
        component_type="pier",
        component_params={"diameter": 800, "height": 3000,
                          "center_x": 0.0, "center_y": 0.0,
                          "z_bottom": z_top_pier - 3000},
        main_rebar_dia=16,
        main_rebar_spacing=150,
        transverse_rebar_dia=8,
        transverse_rebar_spacing=200,
        cover=40,
    )

    main_bars = rebar["rebar_main"]
    trans_bars = rebar["rebar_transverse"]
    print(f"  Main rebar count: {len(main_bars)}")
    print(f"  Transverse rebar count: {len(trans_bars)}")
    assert len(main_bars) > 0, "No main rebar generated"
    assert len(trans_bars) > 0, "No transverse rebar generated"

    pier_bb = get_bounding_box(pier_shape)
    for i, bar in enumerate(main_bars):
        bar_bb = get_bounding_box(bar)
        assert bar_bb[0] >= pier_bb[0] - 1.0, f"Main bar {i} extends beyond pier X-min"
        assert bar_bb[3] <= pier_bb[3] + 1.0, f"Main bar {i} extends beyond pier X-max"
        assert bar_bb[2] >= pier_bb[2] - 1.0, f"Main bar {i} extends beyond pier Z-min"
        assert bar_bb[5] <= pier_bb[5] + 1.0, f"Main bar {i} extends beyond pier Z-max"

    print("  STEP 5 PASSED\n")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--step", type=int, default=0, help="Run specific step (1-5), 0=all available")
    args = parser.parse_args()

    tests = {
        1: test_pier,
        2: test_pier_cap,
        3: test_pile_cap,
        4: test_piles,
        5: test_reinforcement,
    }

    if args.step > 0:
        tests[args.step]()
    else:
        for step_num, test_fn in tests.items():
            try:
                test_fn()
            except Exception as e:
                print(f"  STEP {step_num} FAILED: {e}")
                break
