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
from sheepnado.curve_utils import *
from sheepnado.rig import SheepnadoRig

class SheepnadoDeformCurve(SheepnadoComponent, bpy.types.PropertyGroup):
    object_type = 'CURVE'
    curve_type = 'CURVE'
    
    def draw(self, layout, context):
        pass

    def setup_points(self, spline, num_points):
        dz = -1.0 / (num_points - 1)
        for k, pt in enumerate(spline.bezier_points):
            pt.handle_left_type = 'AUTO'
            pt.handle_right_type = 'AUTO'
            
            pt.co = Vector((0.0, 0.0, dz*k))

    def verify(self, ob, settings, context):
        curve = ob.data
        
        # curve needs to be 3D
        curve.dimensions = '3D'
        
        num_points = settings.rig.handles
        
        verify_curve_bezier_splines(curve, 1, num_points)
        self.setup_points(curve.splines[0], num_points)

    def link(self, ob, settings):
        rig = settings.get_component_type(SheepnadoRig)
        
