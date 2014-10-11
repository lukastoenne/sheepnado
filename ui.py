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
from bpy.types import Panel
from sheepnado.group_utils import get_group

class SheepnadoPanel(Panel):
    """Settings for tornado components"""
    bl_label = "Sheepnado"
    bl_idname = "OBJECT_PT_sheepnado"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    
    @classmethod
    def poll(cls, context):
        ob = context.object
        return ob
    
    def draw(self, context):
        group = get_group(context)
        
        layout = self.layout
        layout.operator("group.sheepnado_verify")
        
        if group:
            group.sheepnado.draw(layout, context)

def register():
    bpy.utils.register_class(SheepnadoPanel)

def unregister():
    bpy.utils.unregister_class(SheepnadoPanel)
