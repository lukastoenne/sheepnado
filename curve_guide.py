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

class SheepnadoCurveGuide(SheepnadoComponent, bpy.types.PropertyGroup):
    object_type = 'CURVE'
    curve_type = 'CURVE'
    
    revolutions = FloatProperty(name="Revolutions", description="Number of revolutions of the curve guide",
                                default=4, min=1.0, soft_min=1.0, soft_max=200.0,
                                update=SheepnadoComponent.component_update)
    resolution = IntProperty(name="Resolution", description="Number of points per curve guide revolution",
                             default=4, min=1, soft_min=3, soft_max=32, options=set(),
                             update=SheepnadoComponent.component_update)
    
    def draw(self, layout, context):
        layout.prop(self, "revolutions")
        layout.prop(self, "resolution")

    def setup_points(self, spline):
        num_points = len(spline.bezier_points)
        num_rev = self.revolutions
        dz = -1.0 / num_points
        dphi = 2*pi * num_rev / num_points
        
        for k, pt in enumerate(spline.bezier_points):
            pt.handle_left_type = 'AUTO'
            pt.handle_right_type = 'AUTO'
            
            pt.co = Vector((sin(dphi*k), cos(dphi*k), dz*k))
    
    def verify(self, ob):
        curve = ob.data
        
        # curve needs to be 3D
        curve.dimensions = '3D'
        
        num_rev = self.revolutions
        num_points = self.resolution * num_rev
        
        if len(curve.splines) != 1:
            curve.splines.clear()
            spline = None
        else:
            spline = curve.splines[0]
            if len(spline.bezier_points) != num_points:
                curve.splines.clear()
                spline = None
        if not spline:
            spline = curve.splines.new('BEZIER')
            spline.bezier_points.add(num_points)
        
        self.setup_points(spline)
