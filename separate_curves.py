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
    "version": (1, 1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Tools Panel > Tools Tab > Edit",
    "warning": "",
    "description": "Separate active curve object by loose parts",
    "category": "Curve",
}


import bpy
from bpy.types import Operator


class SCO_OT_operator(bpy.types.Operator):
    """Separate active curve object by loose parts"""
    bl_idname = "curve.sco"
    bl_label = "By Loose Parts"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active = context.active_object
        if active is None:
            self.report({'WARNING'}, "Select a curve object")
            return {'CANCELLED'}
        else:
            splines = active.data.splines
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.curve.select_all(action = 'DESELECT')

            while len(splines) > 1:
                spline = splines[0]
                if spline.bezier_points:
                    spline.bezier_points[0].select_control_point = True
                elif spline.points:
                    spline.points[0].select = True
                bpy.ops.curve.select_linked()
                bpy.ops.curve.separate()

            bpy.ops.object.mode_set(mode='OBJECT')
            return {'FINISHED'}

class SCO_PT_panel(bpy.types.Panel):
    bl_label = "SCO"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SCO"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'CURVE')

    def draw(self, context):
        layout = self.layout
        layout.operator('curve.sco',text="Separate by loose parts")

classes = (
    SCO_OT_operator,
    SCO_PT_panel,
)

register, unregister = bpy.utils.register_classes_factory(classes)

