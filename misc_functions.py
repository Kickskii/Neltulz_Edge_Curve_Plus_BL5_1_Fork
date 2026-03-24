import bpy
import bmesh

# -----------------------------------------------------------------------------
#   Determine which mode is currently Selected (Vert, Edge, Face, etc)
#   Returned: (0=Multiple modes, 1=Vertice Mode, 2=Edge Mode, 3=Face Mode)
# -----------------------------------------------------------------------------

def getCurrentSelectMode(self, context):
    tempTuple = tuple(context.tool_settings.mesh_select_mode)
    
    if tempTuple == (True, False, False):       
        return 1
    elif tempTuple == (False, True, False):
        return 2
    elif tempTuple == (False, False, True):
        return 3
    
    return 0

def getSelectedVerts(self, context, obj):
    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    return [v.index for v in bm.verts if v.select]

def getSelectedEdges(self, context, obj):
    bm = bmesh.from_edit_mesh(obj.data)
    bm.edges.ensure_lookup_table()
    return [e.index for e in bm.edges if e.select]

def getAllEdges(self, context, obj):
    bm = bmesh.from_edit_mesh(obj.data)
    bm.edges.ensure_lookup_table()
    return [e.index for e in bm.edges]