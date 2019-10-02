# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8-80 compliant>

bl_info = {
    "name": "Separate Curve Object",
    "author": "Agnieszka Pas",
    "version": (2, 1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > SCO Tab > SCO",
    "warning": "",
    "description": "Separate active curve object by loose parts",
    "category": "Curve",
}


import bpy
from bpy.types import Operator, Panel


class SCO_OT_operator(Operator):
    """Separate active curve object by loose parts"""
    bl_idname = "curve.sco"
    bl_label = "By Loose Parts"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layer = context.view_layer
        active = layer.objects.active
        splines = active.data.splines
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.curve.select_all(action='DESELECT')

        while len(splines) > 1:
            spline = splines[0]
            if spline.bezier_points:
                spline.bezier_points[0].select_control_point = True
            elif spline.points:
                spline.points[0].select = True
            bpy.ops.curve.select_linked()
            bpy.ops.curve.separate()

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        return {'FINISHED'}

class SCO_PT_panel(Panel):
    bl_label = "SCO"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SCO"

    @classmethod
    def poll(cls, context):
        active = context.view_layer.objects.active
        return (active and active.type == 'CURVE')

    def draw(self, context):
        layout = self.layout
        layout.label(text="Separate Curve:")
        layout.operator('curve.sco')

classes = (
    SCO_OT_operator,
    SCO_PT_panel,
)

register, unregister = bpy.utils.register_classes_factory(classes)
