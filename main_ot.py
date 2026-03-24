import bpy
from . properties import NTZEDGCRV_ignitproperties
from . import misc_functions
import bmesh
from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

# -----------------------------------------------------------------------------
#    Main Addon Operator
# -----------------------------------------------------------------------------    

class NTZEDGCRV_OT_insertedges(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ntzedgcrv.insertedges"
    bl_label = "Neltulz - Edge Curve"
    bl_description = "Allows you to quick insert edges with flow"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    bForcePanelOptions : BoolProperty(
        name="Force Panel Options",
        description='Gets all of the operator properties from the sidebar panel options.  This will override any settings in the user customized keymap.',
        default = False
    )

    numSegments : IntProperty(
        name="Segment Number",
        description="Number of segments to add. (Default: 1)",
        default = 1,
        min = 1,
        soft_max = 16
    )

    useEdgeFlow : BoolProperty(
        name="Use Edge Flow",
        description='Allows you to use the EdgeFlow options (Tension, Num of iterations, Min Angle).  If this is disabled, then edges will be added without edge flow adjustments. (Default: True)',
        default = True
    )

    showEdgeFlowOptions : BoolProperty(
        name="Show Edge Flow Options",
        default = True
    )

    tension : IntProperty(
        name="Tension",
        description="Tension (Default: 180)",
        default = 180,
        max = 500,
        min = -500
    )

    numIterations : IntProperty(
        name="Number of Iterations",
        description="Number of iterations. (Default: 1)",
        default = 1,
        min = 1,
        soft_max = 128
    )


    minAngle : IntProperty(
        name="Minimum Angle",
        description="Minimum Angle (Default: 0)",
        default = 0,
        max = 180,
        min = 0
    )

    @classmethod
    def poll(cls, context):
        return bpy.context.mode == "EDIT_MESH"


    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        
        col = layout.column(align=True)
        col.prop(self, "numSegments")
        col.prop(self, "useEdgeFlow")

        if self.useEdgeFlow:
            box = col.box().column(align=True)
            box.prop(self, "tension")
            box.prop(self, "numIterations")
            box.prop(self, "minAngle")

    #END draw()

    def execute(self, context):
        scn = context.scene

        selObjs = bpy.context.selected_objects
        activeObjAtBegin = bpy.context.view_layer.objects.active

        try:
            #try to determine objectMode
            modeAtBegin = bpy.context.object.mode
        except:
            modeAtBegin = "OBJECT"

        if activeObjAtBegin is not None:
            if not activeObjAtBegin in selObjs:
                if modeAtBegin == "EDIT":
                    activeObjAtBegin.select_set(True)
                    selObjs.append(activeObjAtBegin)

        

        for obj in selObjs:
            
            #if more than 1 object is selected, then we need to iterate them one at a time.
            if len(selObjs) > 1:
                bpy.ops.object.mode_set(mode='OBJECT') #switch back to object mode
                bpy.ops.object.select_all(action='DESELECT') #deselect all objects
                
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)

            selectedVertIndices = misc_functions.getSelectedVerts(self, context, obj)
            if len(selectedVertIndices) > 0:
                
                selectedEdgeIndices = misc_functions.getSelectedEdges(self, context, obj)
                totalNewEdgeLoopIndices = list()

                for edgeIndex in set(selectedEdgeIndices):
                    # Execute the loopcut
                    bpy.ops.mesh.loopcut(number_cuts=self.numSegments, object_index=0, edge_index=edgeIndex, mesh_select_mode_init=(False, True, False))

                    # Grab the new indices immediately after the cut
                    newEdgeIndices = misc_functions.getSelectedEdges(self, context, obj)
                    totalNewEdgeLoopIndices = list(set(totalNewEdgeLoopIndices).union(set(newEdgeIndices)))

                # Clear old selection
                bpy.ops.mesh.select_all(action='DESELECT')
                
                # Use BMesh to select the newly created edge loops directly in Edit Mode
                bm = bmesh.from_edit_mesh(obj.data)
                bm.edges.ensure_lookup_table()
                
                for i in totalNewEdgeLoopIndices:
                    try:
                        bm.edges[i].select = True
                    except IndexError:
                        pass # Safety catch in case topology indices shifted
                
                # Flush the selection update back to the viewport
                bmesh.update_edit_mesh(obj.data)
                
                # Detect if EdgeFlow addon is installed and execute it
                if self.useEdgeFlow:
                    try:
                        # Patch EdgeFlow's class in memory to bypass the AttributeError
                        if hasattr(bpy.types, "MESH_OT_set_edge_flow"):
                            bpy.types.MESH_OT_set_edge_flow.is_invoked = False
                        
                        # Call normally (EXEC_DEFAULT). This forces EdgeFlow to initialize safely
                        # without overwriting our variables with its defaults.
                        bpy.ops.mesh.set_edge_flow(tension=self.tension, iterations=self.numIterations, min_angle=self.minAngle)
                    except Exception as e:
                        self.report({'ERROR'}, f'EdgeFlow failed: {str(e)}')


        #reselect all originally selected objects, and then set the active object as the original active object
        if len(selObjs) > 1:
            bpy.ops.object.mode_set(mode='OBJECT') #switch back to object mode
            bpy.ops.object.select_all(action='DESELECT') #deselect all objects

            for obj in selObjs:
                obj.select_set(True)

            bpy.context.view_layer.objects.active = activeObjAtBegin

            #switch to edit mode
            bpy.ops.object.mode_set(mode='EDIT')

        #final step - Reset bForcePanelOptions so that it doesn't interfere when it is not explicitly set via keymap
        self.bForcePanelOptions = False

        return {'FINISHED'}
    # END execute()

    def invoke(self, context, event):
        scn = context.scene
        
        if self.bForcePanelOptions:

            if scn.ntzedgcrv.customEdgeCurveSettings == "USE":
            
                self.numSegments    = scn.ntzedgcrv.numSegmentsSlider
                self.useEdgeFlow    = scn.ntzedgcrv.useEdgeFlowCheckbox
                self.tension        = scn.ntzedgcrv.tensionSlider
                self.numIterations  = scn.ntzedgcrv.numIterationsSlider
                self.minAngle       = scn.ntzedgcrv.minAngleSlider

        return self.execute(context)
    #END invoke()

# END Operator()