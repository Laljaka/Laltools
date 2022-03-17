bl_info = {
    "name": "Laltools",
    "author": "Laljaka",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "location": "View3D > Object > HighPoly Ready",
    "description": "Makes your mesh highpoly ready",
    "warning": "",
    "doc_url": "",
    "category": "",
}


import bpy
from props import *
from ops import *
    

class LaltoolsSharpenPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Sharpen"
    bl_idname = "LALTOOLS_PT_sharpen_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Laltools"
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'MESH'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        laltools = scene.laltools
        mesh = context.active_object.data
        
        layout.prop(laltools, 'collapse_modifiers_bool')
        layout.prop(mesh, 'auto_smooth_angle', text='Sharpen angle')
        layout.operator(SharpenButtonOperator.bl_idname, text="Sharpen", icon='SPHERE')
        

class CustomPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "To HighPoly"
    bl_idname = "LALTOOLS_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Laltools"
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        laltools = scene.laltools
        mesh = context.active_object.data
        
        layout.prop(laltools, 'switch_to_sculpt_bool')
        
        row = layout.row(align = True)
        row.prop(laltools, 'subsurf_bool')
        
        sub = row.row()
        sub.enabled = laltools.subsurf_bool == True
        sub.prop(laltools, 'subsurf_level_int')
        
        layout.prop(mesh, 'remesh_voxel_size')
        layout.operator(ButtonOperator.bl_idname, text="Generate", icon='SPHERE')


_classes = [
    MyProperties,
    ButtonOperator,
    SharpenButtonOperator,
    LaltoolsSharpenPanel,
    CustomPanel
]


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.laltools = bpy.props.PointerProperty(type=MyProperties)


def unregister():
    for cls in _classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.laltools


if __name__ == "__main__":
    register()
