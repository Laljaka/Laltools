import bpy

MODES = {
    'EDIT_MESH': 'EDIT',
    'EDIT_CURVE': 'EDIT',
    'EDIT_SURFACE': 'EDIT',
    'EDIT_TEXT': 'EDIT',
    'EDIT_ARMATURE': 'EDIT',
    'EDIT_METABALL': 'EDIT',
    'EDIT_LATTICE': 'EDIT',
    'POSE': 'OBJECT',
    'SCULPT': 'SCULPT',
    'PAINT_WEIGHT': 'WEIGHT_PAINT',
    'PAINT_VERTEX': 'VERTEX_PAINT',
    'PAINT_TEXTURE': 'TEXTURE_PAINT',
    'PARTICLE': 'OBJECT',
    'OBJECT': 'OBJECT',
    'PAINT_GPENCIL': 'SCULPT',
    'EDIT_GPENCIL': 'SCULPT',
    'SCULPT_GPENCIL': 'SCULPT',
    'WEIGHT_GPENCIL': 'WEIGHT_PAINT',
    'VERTEX_GPENCIL': 'VERTEX_PAINT'
}

class MyProperties(bpy.types.PropertyGroup):
    
    subsurf_level_int: bpy.props.IntProperty(name='Level', description='Subsurf level', default=2, min=1)
    
    subsurf_bool: bpy.props.BoolProperty(name='Use subsurf', description='Applies subdivision before remeshing', default=True)
    
    switch_to_sculpt_bool: bpy.props.BoolProperty(name='Switch to sculpt mode', description='Switches to sculpt mode with "Face Set Edit" tool active after remeshing and generating face sets', default=False)
    
    collapse_modifiers_bool: bpy.props.BoolProperty(name = 'Collapse modifiers', description='Applies all modifiers before Sharpen', default = True)
    