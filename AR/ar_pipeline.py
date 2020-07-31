import bpy
import os

# switch on nodes and get reference
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree

   
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


def prepare_camera(img_name, focal=21):
    """
    
    This function creates a camera for rendering.
    :param img_name: name of the background image
    :param focal: focal length of the camera
 
 
    """
    
    scene = bpy.context.collection
    if bpy.data.objects.get("Camera") is not None:
        bpy.data.objects.remove(bpy.data.objects["Camera"],do_unlink=True)
    cam_data = bpy.data.cameras.new('Camera')
    cam_data.lens = focal
    cam = bpy.data.objects.new('Camera', cam_data)
    scene.objects.link(cam)
    bpy.context.scene.camera = cam

    cam.data.show_background_images = True
    bg = cam.data.background_images.new()
    bg.image = bpy.data.images[img_name]

    cam.location = (0, 0, 0)
    cam.rotation_mode = 'XYZ'
    cam.rotation_euler = (0, 3.1416, 3.1416)
    

def prepare_sun_light(location, rotation, energy=8, color=(1,1,1)):
    """
    
    This function creates a sun light source for rendering.
    :param location: location of the sun light
    :param rocation: angles of the light, degree angels should be given
    :param energy: energy of the light, shadow catcher can be seen if not strong enough
    :param color: color of the light 

    """
    if bpy.data.objects.get("Sun") is not None:
        bpy.data.objects.remove(bpy.data.objects["Sun"],do_unlink=True)
        
    bpy.ops.object.light_add(type="SUN")
    light_ob = bpy.context.object
    light_ob.location = location
    light_ob.rotation_euler = (rotation[0]*3.1416/180, rotation[1]*3.1416/180, rotation[2]*3.1416/180)
    light = light_ob.data
    light.energy = energy
    light.color = color


def prepare_ground(location=(0,0,0), rotation= (3.1416/2,0,0), size=30):
    """
    
    This function creates a plane mesh, which is a holder for shadow of the augmented object.


    """
    
    if bpy.data.objects.get("Plane") is not None:
        bpy.data.objects.remove(bpy.data.objects["Plane"],do_unlink=True)

    ground = bpy.ops.mesh.primitive_plane_add(size=size, enter_editmode=False, align='WORLD', location=location, rotation=rotation)


def place_object(location, rotation, obj_path):
    # TODO: set location and rotation of the object we want to place, then it will place the object at that pose.
    pass

def import_scene(path):
    # TODO: import 3D scene, I think it might be better to call pcl_visualizer 
    pass


def render(resolution_x, resolution_y, focal, ground_location, sun_location, sun_rotation, source_img_path, sun_energy=10):
    
    # input a background image for rendering, and create output path accordingly
    
    img = bpy.data.images.load(source_img_path)
    img_name = source_img_path.split("/")[-1]
    dir_path = os.path.dirname(source_img_path)
    out_path = os.path.join(dir_path, "augmented_"+img_name)
    
    # create ground, camera, sun light source for rendering
    
    prepare_ground(location=ground_location)
    prepare_camera(img_name, focal)    
    prepare_sun_light(location=sun_location,rotation=sun_rotation, energy = sun_energy)
    
    # create shadowcatcher material and compositor for rendering
    
    create_shadowcatcher("shadow_catcher")
    create_compositor(img_name)  
    
    # assign the shadowcatcher material to ground, so that it will not be seen after rendering
    
    catcher = bpy.data.objects['Plane']    
    assign_material(catcher, "shadow_catcher")
    
    # start rendering
    
    bpy.context.scene.render.resolution_x = resolution_x
    bpy.context.scene.render.resolution_y = resolution_y
    bpy.context.scene.render.filepath = out_path
    bpy.context.scene.render.film_transparent = True
    bpy.ops.render.render(write_still = True)
    
    
def main():
    
    # From GUI Input
    source_img_path = "I://Dense-Monocular-3D-Mapping-for-AR//ar_pipeline//city1.png"  
    ground_location = (0,0.15,0.0)
    focal=21
    sun_location = (0,-1.8,0)
    sun_rotation = (173,41.4,127)
    resolution_x, resolution_y = (1241, 376)
     
    # Press Render Button!    
    render(resolution_x, resolution_y, focal, ground_location, sun_location, sun_rotation, source_img_path)
    
if __name__ == '__main__':
    main()