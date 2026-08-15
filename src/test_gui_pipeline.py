import sys
import os

with open("C:/Users/neela/OneDrive/Desktop/OsdagBridge/src/test_output.txt", "w") as f:
    try:
        from PySide6.QtWidgets import QApplication
        from osdagbridge.desktop.ui.template_page import CustomWindow
        from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge
        f.write("Imports successful\n")

        app = QApplication(sys.argv)
        f.write("App created\n")
        
        window = CustomWindow("OsdagBridge", PlateGirderBridge)
        f.write("Window created\n")
        
        params = window.backend.get_3d_cad_parameters()
        f.write("Params fetched\n")
        
        window.cad_3d_widget.render_3d_cad(params)
        f.write("Rendered\n")

        viewer = window.cad_3d_widget.viewer
        f.write(f"Pier Caps registered: {len(viewer.model_ais_objects.get('Pier Cap', []))}\n")
        if len(viewer.model_ais_objects.get("Pier Cap", [])) > 0:
            ais = viewer.model_ais_objects["Pier Cap"][0]
            f.write(f"Pier Cap Transparency: {ais.Transparency()}\n")
        f.write(f"Rebar registered: {len(viewer.model_ais_objects.get('Rebar', []))}\n")
    except Exception as e:
        import traceback
        f.write(f"Error: {e}\n{traceback.format_exc()}\n")
