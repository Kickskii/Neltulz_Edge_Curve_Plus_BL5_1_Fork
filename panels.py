import bpy
from bpy.types import Panel

class NTZEDGCRV_PT_sidebarpanel(Panel):
    bl_label = "Edge Curve Plus"
    bl_idname = "NTZEDGCRV_PT_sidebarpanel"
    bl_category = "Neltulz"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw_header(self, context):
        # Adds a nice curve icon directly into the panel title header
        self.layout.label(text="", icon='MOD_CURVE')

    def draw(self, context):
        layout = self.layout
        
        addon_name = __name__.split('.')[0]
        prefs = context.preferences.addons[addon_name].preferences
        is_compact = (prefs.sidebarPanelSize != "DEFAULT")

        # Huge, chunky main action button
        row = layout.row(align=True)
        row.scale_y = 1.0 if is_compact else 1.8 
        row.operator('ntzedgcrv.insertedges', text="Insert Edge(s)", icon="OUTLINER_OB_CURVE")

class NTZEDGCRV_PT_options(Panel):
    bl_label = "Edge Curve Settings"
    bl_idname = "NTZEDGCRV_PT_options"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "NTZEDGCRV_PT_sidebarpanel" # Native collapsible sub-panel
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        layout.use_property_split = True
        
        # Kill the keyframe buttons
        layout.use_property_decorate = False 

        col = layout.column(align=True)
        
        # Big dropdown selector
        col.prop(scn.ntzedgcrv, "customEdgeCurveSettings", text="")
        
        if scn.ntzedgcrv.customEdgeCurveSettings == "USE":
            col.separator(factor=0.5)
            
            box = col.box()
            box_col = box.column(align=True)
            box_col.prop(scn.ntzedgcrv, "numSegmentsSlider", text="Segments")
            
            box_col.separator(factor=0.5)
            
            # Turn the checkbox into a massive, clickable toggle button
            row = box_col.row(align=True)
            row.use_property_split = False
            row.prop(scn.ntzedgcrv, "useEdgeFlowCheckbox", text="Enable Edge Flow", toggle=True, icon='MOD_THICKNESS')

            if scn.ntzedgcrv.useEdgeFlowCheckbox:
                # Nested sleek parameters box
                flow_box = box_col.box()
                flow_box.label(text="Flow Parameters:", icon='IPO_EASE_IN_OUT')
                
                f_col = flow_box.column(align=True)
                f_col.prop(scn.ntzedgcrv, "tensionSlider", text="Tension")
                f_col.prop(scn.ntzedgcrv, "numIterationsSlider", text="Iterations")
                f_col.prop(scn.ntzedgcrv, "minAngleSlider", text="Min Angle")
            
            col.separator(factor=1.0)
            
            reset_row = col.row()
            reset_row.scale_y = 1.2
            reset_row.operator('ntzedgcrv.resetsettings', text="Reset to Defaults", icon="LOOP_BACK").settingToReset = "ALL"