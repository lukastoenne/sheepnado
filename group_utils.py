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
from bpy.types import PropertyGroup, Group, Operator
from bpy.props import *

from sheepnado import curve_guide, rig

_group_name = "SheepnadoGroup"
_object_prefix = "Sheepnado."
_components = {
    ("curve_guide", curve_guide.SheepnadoCurveGuide),
    ("rig", rig.SheepnadoRig),
}

def register_component_properties(propgroup):
    for c in _components:
        bpy.utils.register_class(c[1])
        setattr(propgroup, c[0], PointerProperty(type=c[1]))

def unregister_component_properties(propgroup):
    for c in _components:
        delattr(propgroup, c[0])
        bpy.utils.unregister_class(c[1])

class SheepnadoGroup(PropertyGroup):
    @property
    def components(self):
        """Iterable of tuples (name, settings, object) representing a component"""
        group = self.id_data
        for c in _components:
            yield c[0], getattr(self, c[0], None), group.objects.get(_object_prefix + c[0])

    def get_component_type(self, comptype):
        """Look up tuple (name, settings, object) representing a component"""
        group = self.id_data
        for c in _components:
            if c[1] == comptype:
                return c[0], getattr(self, c[0], None), group.objects.get(_object_prefix + c[0])

    def draw(self, layout, context):
        for c in self.components:
            c[1].draw(layout, context)


# ----------------------------------------------------------------------

def cleanup_group_objects(context, group, cleanup_action):
    settings = group.sheepnado
    
    # map existing objects to component descriptors
    component_objects = { c[2] : c for c in settings.components if c[2] }
    invalid_objects = set(group.objects) - set(component_objects.values())
    
    # remove existing but invalid objects from the list
    for ob, c in component_objects.items():
        if not c[1].poll_object(ob):
            invalid_objects.insert(ob)
    valid_objects = { c[2] : c for c in component_objects.values() if c[2] not in invalid_objects }
    
    # clean up the group
    for ob in invalid_objects:
        if cleanup_action == 'REMOVE':
            group.objects.unlink(ob)
            context.scene.objects.unlink(ob)
            try:
                bpy.data.objects.remove(ob)
            except:
                pass
        elif cleanup_action == 'UNGROUP':
            group.objects.unlink(ob)

def verify_group_objects(context, group, add_missing, cleanup_action):
    settings = group.sheepnado
    
    # remove invalid objects
    cleanup_group_objects(context, group, cleanup_action)
    
    # add missing objects
    for c in settings.components:
        if c[2] is None:
            ob = c[1].create_object(_object_prefix + c[0], context)
            if not ob:
                raise Exception("Could not create component %s" % c[0])
            
            try:
                context.scene.objects.link(ob)
            except:
                pass
            
            try:
                group.objects.link(ob)
            except:
                pass
    
    # verify objects
    for c in settings.components:
        c[1].verify(c[2], context)

def get_group(context):
    return bpy.data.groups.get(_group_name, None)

def verify_group(context):
    group = bpy.data.groups.get(_group_name, None)
    if not group:
        group = bpy.data.groups.new(_group_name)
    return group


class SheepnadoGroupOperator():
    @classmethod
    def poll(cls, context):
        return context.active_object is not None


class SheepnadoGroupVerify(Operator):
    """Verify Sheepnado group"""
    bl_idname = "group.sheepnado_verify"
    bl_label = "Verify Sheepnado"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        group = verify_group(context)
        
        if group:
            verify_group_objects(context, group, True, 'REMOVE')
        
        return {'FINISHED'}

def register():
    register_component_properties(SheepnadoGroup)
    bpy.utils.register_class(SheepnadoGroup)
    Group.sheepnado = PointerProperty(type=SheepnadoGroup)

    bpy.utils.register_class(SheepnadoGroupVerify)

def unregister():
    if Group.sheepnado:
        del Group.sheepnado
    bpy.utils.unregister_class(SheepnadoGroup)
    unregister_component_properties(SheepnadoGroup)

    bpy.utils.unregister_class(SheepnadoGroupVerify)
