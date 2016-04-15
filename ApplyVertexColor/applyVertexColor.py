# ***** BEGIN GPL LICENSE BLOCK *****
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#
# ***** END GPL LICENCE BLOCK *****

bl_info = {
    "name" : "Apply Vertex Color",
    "author" : "Nicolas Liautaud",
    "version" : (1, 0, 0),
    "blender" : (2, 7, 4),
    "description" : "Apply color to selected vertices or faces",
    "category" : "Mesh",}

import bpy
import bmesh

class MESH_xOT_ApplyVertexColor(bpy.types.Operator):
    bl_idname = "mesh.addon_set_vertex_color"
    bl_label = "Set Vertex Color..."
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        mesh = context.object.data
        bm = bmesh.from_edit_mesh(mesh)

        # get or create color layer
        colors = bm.loops.layers.color.active
        if not colors:
            colors = bm.loops.layers.color.new("Col")

        # get Draw brush current color
        color = bpy.data.brushes["Draw"].color

        if tuple(bm.select_mode)[0] == 'FACE':
            # in face mode, assign colors to selected faces loops only (faces color)
            floops = [ l for f in bm.faces for l in f.loops if f.select ]
            for loop in floops:
                loop[colors] = color
        else:
            # assign colors to all loops connected to selected vertices (vertex color)
            vloops = [ l for v in bm.verts for l in v.link_loops if v.select ]
            for loop in vloops:
                loop[colors] = color

        bmesh.update_edit_mesh(mesh)

        return {'FINISHED'}

addon_keymaps = []

def register():

    bpy.utils.register_class(MESH_xOT_ApplyVertexColor)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
    kmi = km.keymap_items.new(MESH_xOT_ApplyVertexColor.bl_idname, 'V', 'PRESS')
    addon_keymaps.append(km)

def unregister():
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()

    bpy.utils.unregister_class(MESH_xOT_ApplyVertexColor)


if __name__ == "__main__":
    register()
