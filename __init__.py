bl_info = {
    "name" : "Make that Clay",
    "blender" : (3,6,1),
    "category" : "3D View",
    "location" : "3D View > Make that Clay",
    "version" : (1,2),
    "author" : "Kent Edoloverio",
    "description" : "Turns mesh into clay",
    "wiki_url" : "https://github.com/kents00/MakethatClay",
    "tracker_url" : "https://github.com/kents00/MakethatClay/issues",
    }

import bpy
import os
from bpy.types import Panel, Operator

class Clay(Operator):
    bl_idname = "material.append_make_that_clay"
    bl_label = "Make that Clay"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self):
        self.source_file = os.path.join(os.path.dirname(__file__), "..", "MakethatClay/data", "Clay.blend")

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'

    def import_file(self):
        if not os.path.isfile(self.source_file):
            self.report({'ERROR'}, "File not found: {}".format(self.source_file))
            return {'CANCELLED'}
        return {'FINISHED'}

    def import_node_group(self, node_group_name):
        with bpy.data.libraries.load(self.source_file, link=False) as (data_from, data_to):
            if node_group_name in data_from.node_groups:
                data_to.node_groups = [node_group_name]

        if not data_to.node_groups or not data_to.node_groups[0]:
            self.report({'ERROR'}, "Failed to load the node group: {}".format(node_group_name))
            self.report({'INFO'}, "Creating new node group: {}".format(node_group_name))

        material = bpy.data.materials.new(name=node_group_name)
        material.use_nodes = True
        if bpy.context.object is not None:
            bpy.context.object.data.materials.append(material)

        tree = material.node_tree
        group_node = tree.nodes.new(type='ShaderNodeGroup')
        group_node.node_tree = data_to.node_groups[0]
        group_node.location = (-40, 300)
        group_node.use_custom_color = True
        group_node.color = (0,0,0)
        group_node.inputs[0].default_value = (0.00151755, 0.043735, 0.0802198, 1)
        group_node.inputs[1].default_value = (1, 0.496933, 0.107023, 1)
        group_node.inputs[2].default_value = 25
        group_node.inputs[3].default_value = 2.5
        group_node.inputs[4].default_value = 0.150
        group_node.inputs[5].default_value = -0.150
        group_node.inputs[6].default_value = 1
        group_node.inputs[7].default_value = 15
        group_node.inputs[8].default_value = -1.2
        group_node.inputs[9].default_value = 0
        group_node.width = 250

        principled_bsdf_node = tree.nodes.get('Principled BSDF')
        if principled_bsdf_node:
            tree.nodes.remove(principled_bsdf_node)

        shader_node_output_material_node = tree.nodes.get('Material Output')
        if shader_node_output_material_node:
            links = tree.links
            links.new(group_node.outputs[0], shader_node_output_material_node.inputs[0])
            links.new(group_node.outputs[1], shader_node_output_material_node.inputs[2])

        self.report({'INFO'}, "Successfully appended node group: {}".format(node_group_name))
        return {'FINISHED'}

    def execute(self,context):
        self.import_file
        self.import_node_group("Makethatclay")
        return {'FINISHED'}

class ClayPanel(Panel):
    bl_label = "Make that Clay"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'TOOLS' if bpy.app.version < (2, 80) else 'UI'
    bl_category = "Make that Clay"
    bl_options = {'HEADER_LAYOUT_EXPAND'}

    def draw(self,context):
        layout = self.layout

        col = layout.row(align=False)
        col.enabled = True
        col.scale_x = 2
        col.scale_y = 2
        col.operator("material.append_make_that_clay")

        col = layout.column(align=False)
        col.label(text=r"SUPPORT ME ON:")
        op = self.layout.operator(
            'wm.url_open',
            text='KO-FI',
            icon='URL'
            )
        op.url = 'https://ko-fi.com/kents_workof_art'

classes = (
    Clay,
    ClayPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
