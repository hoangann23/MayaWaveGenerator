import maya.cmds as cmds
import math
import water_geometry
import water_globals

def animate_water_texture(place2d_node, flow_speed):
    if cmds.objExists('mdNode'):
        md_node = 'mdNode'
    else:
        md_node = cmds.createNode('multiplyDivide', name='mdNode')

    existing = cmds.listConnections(
        f"{md_node}.input1X",
        source=True,
        destination=False,
        plugs=True
    ) or []

    for connection in existing:
        cmds.disconnectAttr(connection, f"{md_node}.input1X")

    cmds.setAttr(f'{md_node}.operation', 1)

    cmds.connectAttr('time1.outTime', f'{md_node}.input1X', force=True)
    cmds.setAttr(f'{md_node}.input2X', flow_speed)

    cmds.connectAttr(f'{md_node}.outputX', f'{place2d_node}.offsetV', force=True)
    cmds.setAttr(f'{place2d_node}.repeatV', 5)

def deform_ribbon_vertices(vertices, normals, time, amplitude, wavelength, speed):
    # return a new list of displaced vertices
    if wavelength <= 0:
        raise ValueError("wavelength must be greater than zero")
    assert(len(vertices) == 2 * len(normals))
    new_vertices = []
    k = (2 * math.pi) / wavelength
    for i in range(len(normals)):
        displacement = amplitude * math.sin((k * i) - (speed * time)) + (amplitude * 0.35) * math.sin((k * 2.3 * i) - (speed * 1.4 * time))
        og_left = vertices[2 * i]
        og_right = vertices[(2*i) + 1]
        norm = normals[i]
        new_left = og_left + (displacement * norm)
        new_right = og_right + (displacement * norm)
        new_vertices.extend([new_left, new_right])
    return new_vertices

def animate_water_geometry(mesh_transform, vertices, normals, amplitude, wavelength, speed):
    current_time = cmds.getAttr('time1.outTime')
    updated_vertices = deform_ribbon_vertices(vertices, normals, current_time, amplitude, wavelength, speed)
    water_geometry.update_ribbon_mesh(mesh_transform, updated_vertices)

def animate_all_water():
    for stream in water_globals.WATER_STREAMS:
        animate_water_geometry(
            stream["mesh"],
            stream["vertices"],
            stream["normals"],
            water_globals.DEFAULT_WAVE_AMP,
            water_globals.DEFAULT_WAVELENGTH,
            water_globals.DEFAULT_WAVE_SPEED)