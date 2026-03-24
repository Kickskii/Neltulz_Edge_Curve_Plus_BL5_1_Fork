import bpy
import os
import webbrowser
from . properties import NTZEDGCRV_ignitproperties
from . import misc_functions

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

# -----------------------------------------------------------------------------
#   Reset Settings
# -----------------------------------------------------------------------------    

class NTZEDGCRV_OT_resetsettings(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ntzedgcrv.resetsettings"
    bl_label = "Neltulz - Edge Curve : Reset Setting(s)"
    bl_description = "Resets setting(s)"

    settingToReset : StringProperty(
        name="Setting to Reset",
        description='Name of the setting to be reset',
        default = "NONE"
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scn = context.scene

        defaultSettingsDict = {
            "numSegmentsSlider"             : 1,
            "useEdgeFlowCheckbox"           : True,
            "tensionSlider"                 : 180,
            "numIterationsSlider"           : 4,
            "minAngleSlider"                : 0,
        }

        if self.settingToReset == "ALL":
            for key in defaultSettingsDict:
                setattr(scn.ntzedgcrv, key, defaultSettingsDict[key])

        elif self.settingToReset != "NONE":
            key = self.settingToReset
            setattr(scn.ntzedgcrv, key, defaultSettingsDict[key])

        return {'FINISHED'}

# -----------------------------------------------------------------------------
#   Open Documentation
# -----------------------------------------------------------------------------

class NTZEDGCRV_OT_opendoc(bpy.types.Operator):
    """Opens the local HTML documentation included with the add-on"""
    bl_idname = "ntzedgcrv.opendoc"
    bl_label = "Open Local Documentation"
    bl_description = "Opens the README_Neltulz_Edge_Curve_Plus.html file in your browser"

    def execute(self, context):
        # Find the directory where this addon is installed
        addon_dir = os.path.dirname(os.path.realpath(__file__))
        
        # Point specifically to your HTML file
        doc_file = "README_Neltulz_Edge_Curve_Plus.html"
        doc_path = os.path.join(addon_dir, doc_file)
        
        if os.path.exists(doc_path):
            # The 'file://' prefix ensures the browser treats it as a local file
            webbrowser.open('file://' + doc_path)
            self.report({'INFO'}, f"Opening {doc_file}")
        else:
            self.report({'ERROR'}, f"File not found: {doc_file}. Please ensure it is in the add-on folder.")
            
        return {'FINISHED'}