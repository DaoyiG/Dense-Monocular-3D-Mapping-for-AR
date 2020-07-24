bl_info = {
    "name": "My Panel",
    "author": "Chendi",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > My Panel",
    "description": "Create my own Panel",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}


import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

PI = 3.1416
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree

class MyPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Layout Demo"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    

    def draw(self, context):
        
        layout = self.layout

        scene = context.scene
        data = bpy.data
        
        # create and set plane
        # set resize
        layout.label(text="Plane Resize: ")
        row = layout.row()
        row.prop(data.objects['Plane'], "scale")
        # set translation
        layout.label(text="Plane Location: ")
        row = layout.row()
        row.prop(data.objects['Plane'], "location")
        # set rotation
        layout.label(text="Plane Rotation: ")
        row = layout.row()
        row.prop(data.objects['Plane'], "rotation_mode")
        row = layout.row()
        row.prop(data.objects['Plane'], "rotation_euler")
        
        # create and set light
        # set translation
        layout.label(text="Light Location: ")
        row = layout.row()
        row.prop(data.objects['Sun'], "location")
        # set rotation
        layout.label(text="Light Rotation: ")
        row = layout.row()
        row.prop(data.objects['Sun'], "rotation_mode")
        row = layout.row()
        row.prop(data.objects['Sun'], "rotation_euler")
        row = layout.row()
        row.prop(data.lights['Sun'], "energy")
        row = layout.row()
        row.prop(data.lights['Sun'], "color")
        
        # import ply
        layout.label(text="Operation1:")
        row = layout.row(align=True)
        row.scale_y = 3.0
        row.operator("import_scene.obj")
        
        # set camera location
        layout.label(text="Camera Settings: ")
        row = layout.row()
        row.prop(scene.camera, "location")
        row = layout.row()
        row.prop(scene.camera, "rotation_mode")
        row = layout.row()
        row.prop(scene.camera, "rotation_euler")
        row = layout.row()
        row.prop(data.cameras[0], "lens")
        
        # set object
        # set resize
        layout.label(text="Object Resize: ")
        row = layout.row()
        row.prop(context.active_object, "scale")
        # set translation
        layout.label(text="Object Location: ")
        row = layout.row()
        row.prop(context.active_object, "location")
        # set rotation
        layout.label(text="Object Rotation: ")
        row = layout.row()
        row.prop(context.active_object, "rotation_mode")
        row = layout.row()
        row.prop(context.active_object, "rotation_euler")
        layout.label(text="Object Metallic: ")
        row = layout.row()
        row.prop(bpy.data.materials["material_0"].node_tree.nodes["Principled BSDF"].inputs["Metallic"], "default_value")
        
        # set render resolution
        layout.label(text="Render resolution: ")
        row = layout.row()
        row.prop(scene.render, "resolution_x")
        row.prop(scene.render, "resolution_y")
        
        # transpatent
        row = layout.row()
        row.prop(scene.render, "film_transparent")
        
        # Big render button
        layout.label(text="Operation2:")
        row = layout.row(align=True)
        row.scale_y = 3.0
        row.operator("render.render")


def register():
    bpy.utils.register_class(MyPanel)


def unregister():
    bpy.utils.unregister_class(MyPanel)


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


def clear_material( material ):
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
    if materials.get( mat_name ) is not None:
        return
    
    material = materials.new( mat_name )
    if not material:
        material = materials.new( mat_name )

    material.use_nodes = True
    clear_material( material )
    for node in material.node_tree.nodes:
        nodes.remove(node) 

    
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    #Some nodes
    diffuse1 = nodes.new( type = 'ShaderNodeBsdfDiffuse' )
    diffuse2 = nodes.new( type = 'ShaderNodeBsdfDiffuse' )

    transp = nodes.new ( type = 'ShaderNodeBsdfTransparent')

    mix = nodes.new ( type = 'ShaderNodeMixShader')

    rgb2bw = nodes.new(type="ShaderNodeRGBToBW")

    s2rgb = nodes.new(type="ShaderNodeShaderToRGB")

    colorramp = nodes.new(type="ShaderNodeValToRGB")

    output = nodes.new( type = 'ShaderNodeOutputMaterial' )

    # Some setting for nodes

    diffuse2.inputs[0].default_value = (0,0,0,1)
    colorramp.color_ramp.elements[0].color = (0,0,0,1)
    colorramp.color_ramp.elements[1].position = (0.5)
    colorramp.color_ramp.elements[1].color = (1, 1, 1, 1)

    #With names
    link1 = links.new( diffuse1.outputs['BSDF'], s2rgb.inputs['Shader'] )
    link2 = links.new( s2rgb.outputs['Color'], rgb2bw.inputs['Color'] )
    link3 = links.new( rgb2bw.outputs['Val'], colorramp.inputs['Fac'] )
    link4 = links.new( colorramp.outputs['Color'], mix.inputs['Fac'] )
    link5 = links.new( diffuse2.outputs['BSDF'], mix.inputs[1] )
    link6 = links.new( transp.outputs['BSDF'], mix.inputs[2] )
    link5 = links.new( mix.outputs['Shader'], output.inputs['Surface'] )

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

    image_node.location = 0,0
    comp_node.location = 400,0

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
    node_tree.nodes["Mapping"].inputs["Rotation"].default_value = (PI/2, PI, PI/2)
    
    # set strength
    node_tree.nodes["Background"].inputs["Strength"].default_value = 0.4



if __name__ == "__main__":
    
    if bpy.data.objects.get("Plane") is None:
        bpy.ops.mesh.primitive_plane_add()
    if bpy.data.objects.get("Light") is not None:
        bpy.data.objects.remove(bpy.data.objects["Light"],do_unlink=True)
    if bpy.data.objects.get("Sun") is None:
        bpy.ops.object.light_add(type="SUN")
        
    
    # set some default first
    bpy.data.objects['Plane'].scale = (10, 10, 10)
    bpy.data.objects['Plane'].rotation_euler = (PI / 2, 0, 0)
    bpy.data.objects['Plane'].location = (0, 0.15, 0)
    
    bpy.data.objects['Sun'].location = (0, -1.8, 0)
    bpy.data.objects['Sun'].rotation_euler = (PI, PI / 4, PI * 0.75)
    bpy.data.lights["Sun"].energy = 16
    bpy.data.lights["Sun"].color = (1, 1, 1)
    
    # TODO: Define exact resolution!
    resolution_x, resolution_y = (1241, 376)
    bpy.context.scene.render.resolution_x = 1392
    bpy.context.scene.render.resolution_y = 512
    
    bpy.data.cameras[0].lens = 21
    bpy.context.scene.camera.location = (0, 0, 0)
    bpy.context.scene.camera.rotation_euler = (0, PI, PI)
    
    source_img_path = "/Users/daoyi/Dense-Monocular-3D-Mapping-for-AR/assets/subscenes/scene1/000020.png"
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
    env_map_path = "/Users/daoyi/Dense-Monocular-3D-Mapping-for-AR/assets/subscenes/scene1/000020.hdr"
    env_map = bpy.data.images.load(env_map_path)
    env_map_name = env_map_path.split("/")[-1]
    create_env_mapping(env_map_name)
    
    # pre_import
    obj_path = "/Users/daoyi/Dense-Monocular-3D-Mapping-for-AR/augmentation_objects/Bus/Bus.obj"
    obj_name = obj_path.split("/")[-1].split(".")[0]
    if bpy.data.objects.get(obj_name) is None:
        Bus = bpy.ops.import_scene.obj(filepath=obj_path)
    
    bpy.data.objects[obj_name].scale = (1e-4, 1e-4, 1e-4)
    bpy.context.view_layer.objects.active = bpy.data.objects[obj_name]
    bpy.data.materials["material_0"].node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 0.5
    if bpy.data.objects.get("Cube") is not None:
        bpy.data.objects.remove(bpy.data.objects["Cube"],do_unlink=True)
    
    # inherit the class(Panel)
    register()
