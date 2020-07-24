# usage: 
# blender -b --python 'auto_ar.py' -- other args

# import auto_ar
import os
import argparse
import sys
import bpy
import numpy as np

PI = 3.1416
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree


class ArgumentParserForBlender(argparse.ArgumentParser):
    """
    This class is identical to its superclass, except for the parse_args
    method (see docstring). It resolves the ambiguity generated when calling
    Blender from the CLI with a python script, and both Blender and the script
    have arguments. E.g., the following call will make Blender crash because
    it will try to process the script's -a and -b flags:
    >>> blender --python my_script.py -a 1 -b 2

    To bypass this issue this class uses the fact that Blender will ignore all
    arguments given after a double-dash ('--'). The approach is that all
    arguments before '--' go to Blender, arguments after go to the script.
    The following calls work fine:
    >>> blender --python my_script.py -- -a 1 -b 2
    >>> blender --python my_script.py --
    """

    def _get_argv_after_doubledash(self):
        """
        Given the sys.argv as a list of strings, this method returns the
        sublist right after the '--' element (if present, otherwise returns
        an empty list).
        """
        try:
            idx = sys.argv.index("--")
            return sys.argv[idx + 1:]  # the list after '--'
        except ValueError as e:  # '--' not in the list:
            return []

    # overrides superclass
    def parse_args(self):
        """
        This method is expected to behave identically as in the superclass,
        except that the sys.argv list will be pre-processed using
        _get_argv_after_doubledash before. See the docstring of the class for
        usage examples and details.
        """
        return super().parse_args(args=self._get_argv_after_doubledash())


def assign_material(obj, materialname):
    """This function assigns a material to an objects mesh.

    :param obj: The object to assign the material to.
    :type obj: bpy.types.Object
    :param materialname: The materials name.
    :type materialname: str

    """
    if materialname not in bpy.data.materials:
        if materialname in defs.defaultmaterials:
            materials.createPhobosMaterials()
        else:
            log("Material to be assigned does not exist.", "ERROR")
            return None
    obj.data.materials.append(bpy.data.materials[materialname])


def clear_material(material):
    """

    This function clear all nodes of a material


    """
    if material.node_tree:
        material.node_tree.links.clear()
        material.node_tree.nodes.clear()


def create_shadowcatcher(name):
    """

    This function creates a shadow catcher, so that shadows of augmented object can be generated during rendering.


    """

    mat_name = name
    materials = bpy.data.materials
    if materials.get(mat_name) is not None:
        return

    material = materials.new(mat_name)
    if not material:
        material = materials.new(mat_name)

    material.use_nodes = True
    clear_material(material)
    for node in material.node_tree.nodes:
        nodes.remove(node)

    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # Some nodes
    diffuse1 = nodes.new(type='ShaderNodeBsdfDiffuse')
    diffuse2 = nodes.new(type='ShaderNodeBsdfDiffuse')

    transp = nodes.new(type='ShaderNodeBsdfTransparent')

    mix = nodes.new(type='ShaderNodeMixShader')

    rgb2bw = nodes.new(type="ShaderNodeRGBToBW")

    s2rgb = nodes.new(type="ShaderNodeShaderToRGB")

    colorramp = nodes.new(type="ShaderNodeValToRGB")

    output = nodes.new(type='ShaderNodeOutputMaterial')

    # Some setting for nodes

    diffuse2.inputs[0].default_value = (0, 0, 0, 1)
    colorramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    colorramp.color_ramp.elements[0].position = 0.4
    colorramp.color_ramp.elements[1].position = 0.6
    colorramp.color_ramp.elements[1].color = (1, 1, 1, 1)

    # With names
    link1 = links.new(diffuse1.outputs['BSDF'], s2rgb.inputs['Shader'])
    link2 = links.new(s2rgb.outputs['Color'], rgb2bw.inputs['Color'])
    link3 = links.new(rgb2bw.outputs['Val'], colorramp.inputs['Fac'])
    link4 = links.new(colorramp.outputs['Color'], mix.inputs['Fac'])
    link5 = links.new(diffuse2.outputs['BSDF'], mix.inputs[1])
    link6 = links.new(transp.outputs['BSDF'], mix.inputs[2])
    link5 = links.new(mix.outputs['Shader'], output.inputs['Surface'])

    material.blend_method = 'BLEND'


def create_compositor(img_name):
    """

    This function creates a compositor for rendering.


    """
    # clear default nodes
    for node in tree.nodes:
        tree.nodes.remove(node)

    # create nodes

    image_node = tree.nodes.new(type='CompositorNodeImage')

    layer_node = tree.nodes.new(type='CompositorNodeRLayers')

    converter = tree.nodes.new(type="CompositorNodeAlphaOver")

    comp_node = tree.nodes.new('CompositorNodeComposite')

    image_node.image = bpy.data.images[img_name]

    image_node.location = 0, 0
    comp_node.location = 400, 0

    # link nodes
    links = tree.links
    link1 = links.new(image_node.outputs[0], converter.inputs[1])
    link2 = links.new(layer_node.outputs[0], converter.inputs[2])
    link3 = links.new(converter.outputs[0], comp_node.inputs[0])


def create_env_mapping(env_map_name):
    # environment texture node
    node_tree = bpy.context.scene.world.node_tree

    if len(node_tree.nodes) > 2:
        return

    enode = node_tree.nodes.new("ShaderNodeTexEnvironment")
    #    enode.image = bpy.data.images.load("/home/chendi/Downloads/city1.hdr")
    enode.image = bpy.data.images[env_map_name]
    node_tree.links.new(enode.outputs['Color'], node_tree.nodes['Background'].inputs['Color'])
    # translation node
    tnode = node_tree.nodes.new(type="ShaderNodeMapping")
    link_t_e = node_tree.links.new(tnode.outputs['Vector'], enode.inputs['Vector'])
    # textture coordinate node
    cnode = node_tree.nodes.new("ShaderNodeTexCoord")
    link_c_t = node_tree.links.new(cnode.outputs['Generated'], tnode.inputs['Vector'])

    # set env map rotation
    node_tree.nodes["Mapping"].inputs["Rotation"].default_value = (PI / 2, PI, PI / 2)

    # set strength
    node_tree.nodes["Background"].inputs["Strength"].default_value = 1


def main(source_img_path, env_map_path, obj_dir, obj_name, out_path,
         obj_location=None, obj_rotation=None, light_rotation=None):
    if bpy.data.objects.get("Plane") is None:
        bpy.ops.mesh.primitive_plane_add()
    if bpy.data.objects.get("Light") is not None:
        bpy.data.objects.remove(bpy.data.objects["Light"], do_unlink=True)
    if bpy.data.objects.get("Sun") is None:
        bpy.ops.object.light_add(type="SUN")

    # set some default first
    bpy.data.objects['Plane'].scale = (10, 10, 10)
    bpy.data.objects['Plane'].rotation_euler = (PI / 2, 0, 0)
    bpy.data.objects['Plane'].location = (0, 0.15, 0)

    bpy.data.objects['Sun'].location = (0, -1.8, 0)
    if light_rotation is None:
        bpy.data.objects['Sun'].rotation_euler = (PI, PI / 4, PI * 0.75)
    else:
        bpy.data.objects['Sun'].rotation_euler = light_rotation
    bpy.data.lights["Sun"].energy = 16
    bpy.data.lights["Sun"].color = (1, 1, 1)

    bpy.context.scene.render.resolution_x = 1241
    bpy.context.scene.render.resolution_y = 376

    bpy.data.cameras[0].lens = 21
    bpy.context.scene.camera.location = (0, 0, 0)
    bpy.context.scene.camera.rotation_euler = (0, PI, PI)

    img = bpy.data.images.load(source_img_path)
    img_name = source_img_path.split("/")[-1]
    bpy.data.cameras[0].show_background_images = True
    bg = bpy.data.cameras[0].background_images.new()
    bg.image = bpy.data.images[img_name]

    bpy.context.scene.render.film_transparent = True

    create_shadowcatcher("shadow_catcher")
    create_compositor(img_name)

    catcher = bpy.data.objects['Plane']
    assign_material(catcher, "shadow_catcher")

    # environment mapping
    env_map = bpy.data.images.load(env_map_path)
    env_map_name = env_map_path.split("/")[-1]
    create_env_mapping(env_map_name)

    # pre_import
    if bpy.data.objects.get(obj_name) is None:
        path = os.path.join(obj_dir, obj_name + ".obj")
        bpy.ops.import_scene.obj(filepath=path)

    if obj_rotation is not None:
        bpy.data.objects[obj_name].rotation_euler = obj_rotation

    if obj_location is None:
        bpy.data.objects[obj_name].location = (0, 0.09, 1.15)
    else:
        bpy.data.objects[obj_name].location = obj_location
    if obj_name == "chev":
        bpy.data.objects[obj_name].location[1] = 0.06

    bpy.context.view_layer.objects.active = bpy.data.objects[obj_name]
    bpy.data.materials[1].node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 0.5

    if bpy.data.objects.get("Cube") is not None:
        bpy.data.objects.remove(bpy.data.objects["Cube"], do_unlink=True)

    bpy.context.scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)


def get_global_args():
    parser = ArgumentParserForBlender()

    parser.add_argument("--obj_dir",
                        help="dir to augment object: ",
                        default="/home/chendi/PycharmProjects/Dense-Monocular-3D-Mapping-for-AR/ar_pipeline/scaled_objs")
    parser.add_argument("--obj",
                        help="select obj: Bus / chev")
    parser.add_argument("--bg",
                        help="path to camera background image: .png",
                        default="/home/chendi/PycharmProjects/Dense-Monocular-3D-Mapping-for-AR/ar_pipeline/subscenes/")
    parser.add_argument("--env",
                        help="path to mapping environment: .hdr",
                        default="/home/chendi/PycharmProjects/Dense-Monocular-3D-Mapping-for-AR/ar_pipeline/hdrs/")
    parser.add_argument("--out",
                        help="path to output image: .jpg",
                        default="/home/chendi/PycharmProjects/Dense-Monocular-3D-Mapping-for-AR/ar_pipeline/outputs/")
    parser.add_argument("--pose",
                        help="path to poses: .txt",
                        default="/home/chendi/PycharmProjects/Dense-Monocular-3D-Mapping-for-AR/ar_pipeline/poses/")
    parser.add_argument("--light",
                        help="rotation of light source",
                        default="/home/chendi/PycharmProjects/Dense-Monocular-3D-Mapping-for-AR/ar_pipeline/light.txt")
    parser.add_argument("--stride",
                        help="stride for the follow up distance",
                        default=10)
    args = parser.parse_args()
    return args.bg, args.env, args.stride, args.pose, args.obj_dir, args.obj, args.out, args.light


def rot2eul(R):
    beta = -np.arcsin(R[2, 0])
    alpha = np.arctan2(R[2, 1] / np.cos(beta), R[2, 2] / np.cos(beta))
    gamma = np.arctan2(R[1, 0] / np.cos(beta), R[0, 0] / np.cos(beta))
    return np.array((alpha, beta, gamma))


def eul2rot(theta):
    R = np.array([[np.cos(theta[1]) * np.cos(theta[2]),
                   np.sin(theta[0]) * np.sin(theta[1]) * np.cos(theta[2]) - np.sin(theta[2]) * np.cos(theta[0]),
                   np.sin(theta[1]) * np.cos(theta[0]) * np.cos(theta[2]) + np.sin(theta[0]) * np.sin(theta[2])],
                  [np.sin(theta[2]) * np.cos(theta[1]),
                   np.sin(theta[0]) * np.sin(theta[1]) * np.sin(theta[2]) + np.cos(theta[0]) * np.cos(theta[2]),
                   np.sin(theta[1]) * np.sin(theta[2]) * np.cos(theta[0]) - np.sin(theta[0]) * np.cos(theta[2])],
                  [-np.sin(theta[1]), np.sin(theta[0]) * np.cos(theta[1]), np.cos(theta[0]) * np.cos(theta[1])]])

    return R


if __name__ == "__main__":

    img_dir, hdr_dir, stride, pose_dir, obj_dir, obj_name, out_dir, light_dir = get_global_args()
    scenes = sorted(os.listdir(img_dir))
    scenes = [scenes[0]]  # only for debugging
    poses_file = sorted(os.listdir(pose_dir))
    light_rots = np.loadtxt(light_dir)
    light_rots = light_rots / 180 * PI

    for idx, scene in enumerate(scenes):
        imgs = sorted(os.listdir(os.path.join(img_dir, scene)))
        for img in imgs[0:-1 - stride]:
            img_num = int(img.split('.')[0])
            pose1 = np.loadtxt(pose_dir + poses_file[img_num]).reshape(3, 4)
            pose1 = np.vstack([pose1, [0., 0., 0., 1.]])
            pose2 = np.loadtxt(pose_dir + poses_file[img_num + stride]).reshape(3, 4)
            pose2 = np.vstack([pose2, [0., 0., 0., 1.]])
            pose = np.matmul(np.linalg.inv(pose1), pose2)
            obj_location = (pose[0, 3] / 10, 0.09, pose[2, 3] / 10)

            rot = np.matmul(pose[0:3, 0:3], eul2rot((PI / 2, 0, 0)))
            rotation = rot2eul(rot)

            source_img_path = os.path.join(img_dir, scene, img)
            env_map_path = os.path.join(hdr_dir, scene, img.split('.')[0] + '.hdr')
            out_path = os.path.join(out_dir, scene, img.split('.')[0] + '.jpg')

            main(source_img_path, env_map_path, obj_dir, obj_name, out_path,
                 obj_location, rotation, tuple(light_rots[idx, :]))
