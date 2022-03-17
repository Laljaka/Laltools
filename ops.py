import bpy
import bmesh
from props import MODES


class SharpenButtonOperator(bpy.types.Operator):
    """Sharpens"""
    bl_idname = "laltools.sharpen_operator"
    bl_label = "Sharpen object"
    bl_options = {'REGISTER', 'UNDO'}
    
    edge_angle = {}
    mode = None
    
    sharpen_agnle: bpy.props.FloatProperty(name='Sharpen angle', default=0.523599, min=0, max=3.141593, precision=6, step=10, unit='ROTATION')
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and (context.active_object.type == 'MESH' and len(context.selected_objects) != 0)
    
    def invoke(self, context, event):
        self.edge_angle = {}
        self.mode = context.mode
        me = context.active_object.data
        ob = context.active_object
        
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        bpy.ops.object.shade_smooth()
        ob.data.use_auto_smooth = True

        if context.scene.laltools.collapse_modifiers_bool:
            for _, m in enumerate(ob.modifiers):
                bpy.ops.object.modifier_apply(modifier=m.name)
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bm = bmesh.from_edit_mesh(me)
        
        for face in bm.faces:
            for edge in face.edges:
                faces = []
                for linked_face in edge.link_faces:
                    faces.append(linked_face)
                angle = faces[0].normal.angle(faces[1].normal)
                self.edge_angle[edge.index] = angle
        
        self.sharpen_agnle = ob.data.auto_smooth_angle
        
        return self.execute(context)
    
    def execute(self, context):
                
        ob = context.active_object
        
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        for edge in ob.data.edges:
            if self.edge_angle[edge.index] >= self.sharpen_agnle:
                edge.use_edge_sharp = True
            else:
                edge.use_edge_sharp = False
                
        ob.data.auto_smooth_angle = self.sharpen_agnle
        
        bpy.ops.object.mode_set(mode=MODES[self.mode])
        return {'FINISHED'}
    

class ButtonOperator(bpy.types.Operator):
    """Remesh and generate face sets. Applies all modifiers in order by default"""
    bl_idname = "laltools.convert_operator"
    bl_label = "Prepare Face Sets"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and (context.active_object.type == 'MESH' and len(context.selected_objects) != 0)
    
    def execute(self, context):
        laltools = context.scene.laltools
        ob = context.object
        mode = context.mode
        
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        for _, m in enumerate(ob.modifiers):
            bpy.ops.object.modifier_apply(modifier=m.name)
        
        for e in ob.data.edges:
            if e.use_edge_sharp:
                e.crease = 1.0
        
        if laltools.subsurf_bool:
            ob.modifiers.new('Subsurf', 'SUBSURF')
            ob.modifiers['Subsurf'].levels = laltools.subsurf_level_int
            bpy.ops.object.modifier_apply(modifier="Subsurf")
        
        bpy.ops.object.mode_set(mode = 'SCULPT')
        
        bpy.ops.sculpt.face_sets_init(mode='SHARP_EDGES')
        ob.data.use_remesh_preserve_sculpt_face_sets = True
        ob.data.use_remesh_preserve_volume = True
        ob.data.use_remesh_fix_poles = True

        bpy.ops.object.voxel_remesh()
        
        bpy.ops.paint.brush_select(sculpt_tool='MASK')
        bpy.data.brushes["Mask"].strength = 1
        bpy.data.brushes["Mask"].use_automasking_boundary_face_sets = True
        
        verts = [vert.co for vert in ob.data.vertices]
        plain_verts = [vert.to_tuple() for vert in verts]
        
        strokes = []
        for i, p in enumerate(plain_verts):
            stroke = {    
                "name": "stroke",
                "mouse": (0, 0),
                "mouse_event": (0, 0),
                "x_tilt": 0,
                "y_tilt": 0,
                "pen_flip": False,
                "is_start": True,
                "location": p,
                "size": 1.0,
                "pressure": 1.0,
                "time": float(i)
            }
            strokes.append(stroke)
        bpy.ops.sculpt.brush_stroke(stroke=strokes)
        
        bpy.ops.paint.mask_flood_fill(mode='INVERT')
        bpy.ops.sculpt.face_sets_create(mode='MASKED')
        bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0.0)
        
        if laltools.switch_to_sculpt_bool:
            bpy.ops.object.mode_set(mode = 'SCULPT')
            bpy.ops.wm.tool_set_by_id(name='builtin.face_set_edit')
        else:
            bpy.ops.object.mode_set(mode = MODES[mode])
        
        return {'FINISHED'}