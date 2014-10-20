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

# Base class for component property groups
# Implementation classes should derive also from bpy.types.PropertyGroup
# and register in group_utils.
#
# If the poll_object and create_object functions are not overloaded,
# the object_type class attribute must be specified to make sure the
# correct object type is used for the component.
#
# 
class SheepnadoComponent():
    # Test if main object type is correct
    def poll_object(self, ob):
        if ob.type != self.object_type:
            return False
        return True
    
    # Create a new object data block
    def _create_object_data(self, name):
        datatype = self.object_type
        if datatype == 'MESH':
            data = bpy.data.meshes.new(name)
        elif datatype == 'CURVE':
            data = bpy.data.curves.new(name, type=self.curve_type)
        elif datatype == 'ARMATURE':
            data = bpy.data.armatures.new(name)
        else:
            raise Exception("Unsupported object data type %s" % datatype)
            data = None
        return data
    
    # Create a new object
    def create_object(self, name, context):
        from bpy_extras import object_utils
        
        data = self._create_object_data(name)
        ob = object_utils.object_data_add(context, data).object
        # XXX hack: force exact object name by setting it explicitly
        ob.name = name
        
        return ob
    
    # Add custom property drawing here
    def draw(self, layout, context):
        raise Exception("'draw' method not implemented")
    
    # Main object setup here
    def verify(self, ob, settings, context):
        raise Exception("'verify' method not implemented")

    # Create connections to other components
    def link(self, ob, settings):
        pass

    # Update callback for properties to rebuild the object
    def component_update(self, context):
        group = self.id_data
        if group:
            settings = group.sheepnado
            name, settings, ob = settings.get_component_type(type(self))
            if ob:
                self.verify(ob, settings, context)
