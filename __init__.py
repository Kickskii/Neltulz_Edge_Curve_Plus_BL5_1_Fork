bl_info = {
    "name" : "Neltulz - Edge Curve",
    "author" : "Neil V. Moore",
    "description" : "Allows you to quickly insert edge loops with flow (Requires edge flow addon)",
    "blender" : (5, 0, 0),
    "version" : (1, 0, 8),
    "location" : "View3D",
    "warning" : "",
    "category" : "3D View",
    "tracker_url": "https://github.com/YOUR-USERNAME/Edge-Curve-Plus/issues",
    "doc_url": "https://github.com/YOUR-USERNAME/Edge-Curve-Plus/wiki"
}

import bpy

from . properties        import NTZEDGCRV_ignitproperties
from . main_ot           import NTZEDGCRV_OT_insertedges
from . misc_ot           import NTZEDGCRV_OT_resetsettings, NTZEDGCRV_OT_opendoc
from . addon_preferences import NTZEDGCRV_OT_addonprefs
from . panels            import NTZEDGCRV_PT_sidebarpanel
from . panels            import NTZEDGCRV_PT_options

from . import keymaps

bDebugModeActive = False
if bDebugModeActive:
    print("----------------------------------------------------------------------")
    print("REMINDER: Neltulz Edge Curve Debug Mode Active")
    print("----------------------------------------------------------------------")

classes = (
    NTZEDGCRV_ignitproperties,
    NTZEDGCRV_OT_insertedges,
    NTZEDGCRV_OT_resetsettings,
    NTZEDGCRV_OT_opendoc,
    NTZEDGCRV_OT_addonprefs,
    NTZEDGCRV_PT_sidebarpanel,
    NTZEDGCRV_PT_options,
)

addon_keymaps = []

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # update panel name based on preferences
    prefs = bpy.context.preferences.addons[__name__].preferences
    if prefs:
        from . import addon_preferences
        addon_preferences.update_panel(prefs, bpy.context)

    # register keymaps
    keymaps.neltulz_edge_curve_plus_register_keymaps(addon_keymaps)

    # add property group to the scene
    bpy.types.Scene.ntzedgcrv = bpy.props.PointerProperty(type=NTZEDGCRV_ignitproperties)


def unregister():
    # remove keymaps first
    keymaps.neltulz_edge_curve_plus_unregister_keymaps(addon_keymaps)

    # remove properties
    if hasattr(bpy.types.Scene, "ntzedgcrv"):
        del bpy.types.Scene.ntzedgcrv

    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass

if __name__ == "__main__":
    register()