import bpy
from . panels import NTZEDGCRV_PT_sidebarpanel, NTZEDGCRV_PT_options
from bpy.props import StringProperty, EnumProperty
from bpy.types import AddonPreferences

# Define Panel classes for updating
panels = (NTZEDGCRV_PT_sidebarpanel, NTZEDGCRV_PT_options)

def update_panel(self, context):
    addon_name = __name__.split('.')[0]
    if addon_name not in context.preferences.addons:
        return
    prefs = context.preferences.addons[addon_name].preferences

    sidebar_size = prefs.sidebarPanelSize
    category_name = prefs.category

    try:
        # Unregister backwards
        for panel in reversed(panels):
            if hasattr(bpy.types, panel.__name__):
                bpy.utils.unregister_class(panel)

        # Update region/category data
        for panel in panels:
            if sidebar_size == "HIDE":
                panel.bl_category = "Item"
                panel.bl_region_type = "WINDOW"
            else:
                panel.bl_category = category_name
                panel.bl_region_type = "UI"

        # Register forwards
        for panel in panels:
            bpy.utils.register_class(panel)

    except Exception as e:
        print(f"\n[Neltulz Edge Curve] Updating Panel failed: {e}")


class NTZEDGCRV_OT_addonprefs(AddonPreferences):
    bl_idname = __name__.split('.')[0]

    category: StringProperty(
        name="Tab Category",
        description="Choose a name for the category of the panel",
        default="Neltulz",
        update=update_panel,
    )

    sidebarPanelSize : EnumProperty (
        items = [
            ("DEFAULT", "Default", "", "", 0),
            ("COMPACT", "Compact", "", "", 1),
            ("HIDE",    "Hide",    "", "", 2),
        ],
        name = "Sidebar Panel Size",
        description = "Sidebar Panel Size",
        default = "DEFAULT",
        update=update_panel,
    )

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        
        col = layout.column(align=True)
        col.prop(self, "sidebarPanelSize", text="Sidebar Panel Size")
        
        row = col.row(align=True)
        row.enabled = (self.sidebarPanelSize != "HIDE")
        row.prop(self, "category", text="Tab Category Name", icon='OUTLINER_DATA_FONT')
        
        # Fancy Documentation Section
        layout.separator()
        box = layout.box()
        box.label(text="Documentation & Support", icon='HELP')
        box.operator("ntzedgcrv.opendoc", text="Read Local Documentation", icon='FILE_TEXT')