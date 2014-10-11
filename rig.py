### BEGIN GPL LICENSE BLOCK #####
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

# <pep8 compliant>

import bpy
from bpy.props import *
from math import *
from mathutils import *

from sheepnado.component import *

_bone_prefix = "handle"

class SheepnadoRig(SheepnadoComponent, bpy.types.PropertyGroup):
    object_type = 'ARMATURE'
    
    handles = IntProperty(name="Handles", description="Number of handles",
                          default=4, min=2, soft_min=2, soft_max=32, options=set(),
                          update=SheepnadoComponent.component_update)
    
    def setup_bones(self, ob, num_points):
        arm = ob.data
        
        while arm.edit_bones:
            arm.edit_bones.remove(arm.edit_bones[0])
        
        dz = -1.0 / (num_points - 1)
        for i in range(num_points):
            bone = arm.edit_bones.new(_bone_prefix + str(i))
            
            bone.head = Vector((0.0, 0.0, i * dz))
            bone.tail = bone.head + Vector((0.0, 0.0, 1.0))
    
    def draw(self, layout, context):
        layout.prop(self, "handles")

    def verify(self, ob, context):
        cur_act = context.scene.objects.active
        # set the armature as active and go to edit mode to add bones
        context.scene.objects.active = ob
        bpy.ops.object.mode_set(mode='EDIT')
            
        try:
            self.setup_bones(ob, self.handles)
        except Exception:
            raise
        finally:
            bpy.ops.object.mode_set(mode='POSE')
            context.scene.objects.active = cur_act
