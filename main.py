import maya.cmds as cmds
import maya.api.OpenMaya as om
import sys

project_dir = cmds.workspace(query=True, rootDirectory=True)
scripts_dir = project_dir + "scripts/waterAnimator"
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

import importlib
import curve_sampling
import water_geometry
import water_globals
import water_animation

importlib.reload(water_globals)
importlib.reload(curve_sampling)
importlib.reload(water_geometry)
importlib.reload(water_animation)

curve = curve_sampling.get_selected_curve()
waterShader = water_geometry.create_water_material("waterMaterialSG", "waterMaterial")
waterTexture = water_geometry.create_water_texture(waterShader, "waterTexture")
if water_globals.WATER_ANIMATION_JOB is not None:
    om.MMessage.removeCallback(water_globals.WATER_ANIMATION_JOB)
    water_globals.WATER_ANIMATION_JOB = None

if curve:
    curve_points, curve_tangents = curve_sampling.sample_curve(curve, water_globals.DEFAULT_SAMPLE_COUNT)
    if curve_points and curve_tangents:
        mesh_vertices = water_geometry.generate_ribbon_vertices(curve_points, curve_tangents, water_globals.DEFAULT_WIDTH)
        ribbon_normals = water_geometry.generate_ribbon_normals(curve_tangents)
        if mesh_vertices:
            water_mesh = water_geometry.generate_ribbon_mesh(mesh_vertices)
            cmds.sets(water_mesh, edit=True, forceElement=waterShader)
            water_animation.animate_water_texture(waterTexture, 0.02)
            water_globals.WATER_STREAMS.append({
                "mesh": water_mesh,
                "vertices": mesh_vertices,
                "normals": ribbon_normals})
            water_globals.WATER_ANIMATION_JOB = om.MEventMessage.addEventCallback(
                "timeChanged",
                lambda *args: water_animation.animate_all_water())