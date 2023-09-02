bl_info = {
    "name" : "Make that Clay",
    "blender" : (3,6,1),
    "category" : "3D View",
    "location" : "3D View > Make that Clay",
    "version" : (1,2),
    "author" : "Kent Edoloverio",
    "description" : "Turns mesh into clay",
    "wiki_url" : "",
    "tracker_url" : "",
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
        return {'FINISHED'}

    def import_node_group(self, node_group_name):
        with bpy.data.libraries.load(self.source_file, link=False) as (data_from, data_to):
            if node_group_name in data_from.node_groups:
                data_to.node_groups = [node_group_name]

        if not data_to.node_groups or not data_to.node_groups[0]:
            self.report({'ERROR'}, "Failed to load the node group: {}".format(node_group_name))
            self.report({'INFO'}, "Creating new node group: {}".format(node_group_name))
            return {'FINISHED'}

    def execute(self):
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
        image = bpy.data.images.load(os.path.join(os.path.dirname(__file__), "..", "MakethatClay/data", "logo.png"))
        col.image(image, use_pixels_as_ico=True)

        col = layout.row(align=False)
        col.enabled = True
        col.scale_x = 1.2
        col.scale_y = 1.2
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