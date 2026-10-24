import maya.cmds as cmds
import maya.api.OpenMaya as om
import math

def get_selected_curve():
    selected = cmds.ls(selection=True, objectsOnly=True) or []
    if not selected:
        cmds.warning("Please select one NURBS curve.")
        return None

    curve = selected[0]
    shapes = cmds.listRelatives(curve, shapes=True, noIntermediate=True) or []
    is_curve = any(cmds.nodeType(shape) == "nurbsCurve" for shape in shapes)
    if not is_curve:
        cmds.warning("Please select one NURBS curve.")
        return None

    return curve

def sample_curve(curve_transform, sample_count):
    if not isinstance(sample_count, int) or sample_count <= 1:
        cmds.warning("Sample count must be a number greater than one")
        return None, None
    
    if not cmds.objExists(curve_transform):
        cmds.warning("The source curve no longer exists")
        return None, None

    shapes = cmds.listRelatives(curve_transform, shapes=True, noIntermediate=True) or []
    selection = om.MSelectionList()
    for shape in shapes:
        if cmds.nodeType(shape) == "nurbsCurve":
            selection.add(shape)
            break
    else:
        cmds.warning("The source curve was not found")
        return None, None
    dag_path = selection.getDagPath(0)

    curve_fn = om.MFnNurbsCurve(dag_path)
    length = curve_fn.length()
    if not math.isfinite(length) or length <= 1e-6:
        cmds.warning("The source curve must have a non-zero length.")
        return None, None
    sample_space = length / (sample_count - 1)
    points = []
    tangents = []
    last_tangent = om.MVector(0, 0, 1)

    for i in range(sample_count):
        sample_distance = i * sample_space
        parameter = curve_fn.findParamFromLength(sample_distance)
        point = curve_fn.getPointAtParam(parameter, om.MSpace.kWorld)
        points.append(point)
        tangent = curve_fn.tangent(parameter, om.MSpace.kWorld)
        if tangent.length() > 1e-6:
            tangent.normalize()
            last_tangent = tangent
        else:
            tangent = last_tangent
        tangents.append(tangent)

    return points, tangents