import bpy


def create_material(name: str, color):
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
    material.metallic = 0.7
    material.roughness = 0.2

    material.diffuse_color = color
    return material


def make_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def create_camera():
    """
    create and setup the camera
    """
    bpy.ops.object.camera_add(location=(10, 1, 3), rotation=(0, 0, 0))
    camera = bpy.context.active_object

    # set the camera as the "active camera" in the scene
    bpy.context.scene.camera = camera

    # set the Focal Length of the camera
    camera.data.lens = 20

    camera.data.passepartout_alpha = 0.9

    # Create empty object for camera to track
    bpy.ops.object.empty_add(type="PLAIN_AXES", align="WORLD", location=(3.5, 3.5, 0))
    empty_ctrl = bpy.context.active_object
    empty_ctrl.name = "empty.cntrl"

    make_active(camera)
    bpy.ops.object.constraint_add(type="TRACK_TO")
    bpy.context.object.constraints["Track To"].target = empty_ctrl

    return (camera, empty_ctrl)


def create_light():
    bpy.ops.object.light_add(
        type="POINT", radius=10, align="WORLD", location=(-2, -2, 4), scale=(1, 1, 1)
    )
    bpy.context.object.data.energy = 3000

    bpy.ops.object.light_add(
        type="POINT", radius=10, align="WORLD", location=(8, 8, 4), scale=(1, 1, 1)
    )
    bpy.context.object.data.energy = 3000

    bpy.ops.object.light_add(
        type="POINT", radius=10, align="WORLD", location=(3.5, 3.5, 7), scale=(1, 1, 1)
    )
    bpy.context.object.data.energy = 4000

    return bpy.context.active_object
