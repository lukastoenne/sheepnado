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

def verify_curve_bezier_splines(curve, num_splines, num_points, type='BEZIER'):
    clear = False
    for s in curve.splines:
        if len(s.bezier_points) != num_points:
            clear = True
            break
    if clear:
        curve.splines.clear()
    while len(curve.splines) > num_splines:
        curve.splines.remove(curve.splines[0])
    while len(curve.splines) < num_splines:
        s = curve.splines.new('BEZIER')
        #print("spline points : %d" % len(s.bezier_points))

    for s in curve.splines:
        if len(s.bezier_points) < num_points:
            s.bezier_points.add(num_points - len(s.bezier_points))
        # spline should either have right number of points or be empty
        #print("num points : %d vs %d" % (len(s.bezier_points), num_points))
        assert(len(s.bezier_points) == num_points)
