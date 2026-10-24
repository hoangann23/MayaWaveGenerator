import maya.cmds as cmds
import maya.api.OpenMaya as om

def generate_ribbon_normals(tangents):
    normals = []
    world_up = om.MVector(0,1,0)
    for tangent in tangents:
        side = tangent ^ world_up
        if side.length() <= 1e-6:
            side = tangent ^ om.MVector(1,0,0)
        side.normalize()
        normal = side ^ tangent
        normal.normalize()
        normals.append(normal)

    return normals

def generate_ribbon_vertices(points, tangents, width):
    if len(points) != len(tangents):
        cmds.warning("Unequal amount of points and tangents")
        return None

    if width <= 0:
        cmds.warning("width must be greater than zero.")
        return None

    vertices = []
    half_width = width / 2
    world_up = om.MVector(0,1,0)

    for point, tangent in zip(points, tangents):
        # calculate side vector
        side = tangent ^ world_up
        if side.length() <= 1e-6:
            side = tangent ^ om.MVector(1,0,0)
        side.normalize()

        # get side vertices
        p1 = point - (half_width * side)
        p2 = point + (half_width * side)

        vertices.append(p1)
        vertices.append(p2)
    return vertices

def generate_ribbon_mesh(vertices):
    assert(len(vertices) % 2 == 0)
    num_samples = len(vertices) // 2
    face_indices = []
    for i in range(num_samples-1):
        left_i = 2*i
        right_i = 2*i + 1
        next_left = 2*(i+1)
        next_right = 2*(i+1) + 1
        face_indices.extend([left_i, right_i, next_right, next_left])
    mesh_fn = om.MFnMesh()
    mesh_object = mesh_fn.create(vertices, [4]*(num_samples-1), face_indices)
    mesh_transform = om.MFnDagNode(mesh_object).name()

    uvs = generate_ribbon_uvs(num_samples)
    uArray, vArray = zip(*uvs)
    mesh_fn.setUVs(uArray, vArray)
    uvIds = face_indices
    mesh_fn.assignUVs([4] * (num_samples - 1), uvIds)
    return mesh_transform

def update_ribbon_mesh(mesh_transform, vertices):
    shapes = cmds.listRelatives(mesh_transform, shapes=True, noIntermediate=True)
    if shapes:
        selection = om.MSelectionList()
        selection.add(shapes[0])
        dag_path = selection.getDagPath(0)
        mesh_fn = om.MFnMesh(dag_path)
        mesh_fn.setPoints(vertices, om.MSpace.kWorld)

def generate_ribbon_uvs(num_samples):
    assert(num_samples > 1)
    uvs = []
    for i in range(num_samples):
        v = i / (num_samples - 1)
        u_left = 0
        u_right = 1
        uvs.append((u_left, v))
        uvs.append((u_right, v))
    return uvs

def create_water_material(shader_name, material_name):
    if cmds.objExists(material_name):
            waterMaterial = material_name
    else:
        waterMaterial = cmds.shadingNode('lambert', asShader=True, name=material_name)
        cmds.setAttr(waterMaterial + '.color', 0.0, 0.0, 1.0, type='double3')
    if cmds.objExists(shader_name):
        connected_shader = cmds.listConnections(shader_name + ".surfaceShader", source=True, destination=False)
        if connected_shader:
            return shader_name
        waterGroup = shader_name
    else:
        waterGroup = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shader_name)
    
    cmds.connectAttr(waterMaterial + '.outColor', waterGroup + '.surfaceShader', force=True)
    return waterGroup

def create_water_texture(shader_name, texture_name):
    if cmds.objExists(texture_name):
        waterTexture = texture_name
    else:
        waterTexture = cmds.shadingNode('file', asTexture=True, name=texture_name)
    if cmds.objExists(waterTexture+"Place2dTexture"):
        place2d_node = waterTexture+"Place2dTexture"
    else:
        place2d_node = cmds.shadingNode("place2dTexture", asUtility=True, name=waterTexture+"Place2dTexture")
    if cmds.objExists('waterBlend'):
        waterBlend = 'waterBlend'
    else:
        waterBlend = cmds.createNode('blendColors', name='waterBlend')

    cmds.setAttr(f'{waterBlend}.color1', 0.01, 0.12, 0.3, type='double3')
    cmds.setAttr(f'{waterBlend}.color2', 0.15, 0.65, 1.0, type='double3')
    cmds.setAttr(f"{waterTexture}.fileTextureName", "sourceimages/Perlin_noise_example.png", type="string")
    connections = [
        ('outUV', 'uvCoord'),
        ('outUvFilterSize', 'uvFilterSize'),
        ('coverage', 'coverage'),
        ('translateFrame', 'translateFrame'),
        ('rotateFrame', 'rotateFrame'),
        ('mirrorU', 'mirrorU'),
        ('mirrorV', 'mirrorV'),
        ('stagger', 'stagger'),
        ('wrapU', 'wrapU'),
        ('wrapV', 'wrapV'),
        ('repeatUV', 'repeatUV'),
        ('offset', 'offset'),
        ('rotateUV', 'rotateUV'),
        ('noiseUV', 'noiseUV'),
        ('vertexUvOne', 'vertexUvOne'),
        ('vertexUvTwo', 'vertexUvTwo'),
        ('vertexUvThree', 'vertexUvThree')
    ]
    for (x, y) in connections:
        if not cmds.isConnected(f"{place2d_node}.{x}", f"{waterTexture}.{y}"):
            cmds.connectAttr(f"{place2d_node}.{x}", f"{waterTexture}.{y}", force=True)

    
    connected_shader = cmds.listConnections(shader_name + ".surfaceShader", source=True, destination=False)

    if not cmds.isConnected(f"{waterTexture}.outColorR", f"{waterBlend}.blender"):
        cmds.connectAttr(f"{waterTexture}.outColorR", f"{waterBlend}.blender", force=True)

    if not cmds.isConnected(f"{waterBlend}.output", f"{connected_shader[0]}.color"):
        cmds.connectAttr(f"{waterBlend}.output", f"{connected_shader[0]}.color")

    return place2d_node