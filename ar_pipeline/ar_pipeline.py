import bpy


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
            # print("###ERROR: material to be assigned does not exist.")
            log("Material to be assigned does not exist.", "ERROR")
            return None
#    obj.data.materials[0] = bpy.data.materials[materialname]
    obj.data.materials.append(bpy.data.materials[materialname])
#    if bpy.data.materials[materialname].use_transparency:
#        obj.show_transparent = True   


# Clear all nodes in a mat
def clear_material( material ):
    if material.node_tree:
        material.node_tree.links.clear()
        material.node_tree.nodes.clear()



def create_shadowcatecher(name):
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
#        if node.type != 'OUTPUT_MATERIAL': # skip the material output node as we'll need it later
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
    #Or with indices
    #link = links.new( diffuse.outputs[0], output.inputs[0] )
 
def create_compositor(img_name):
    # clear default nodes
    for node in tree.nodes:
        tree.nodes.remove(node)

    # create nodes

    image_node = tree.nodes.new(type='CompositorNodeImage')

    layer_node = tree.nodes.new(type='CompositorNodeRLayers')

    converter = tree.nodes.new(type="CompositorNodeAlphaOver")

    comp_node = tree.nodes.new('CompositorNodeComposite')   
    
#    print(img_name)
    image_node.image = bpy.data.images[img_name]

    image_node.location = 0,0
    comp_node.location = 400,0

    # link nodes
    links = tree.links
    link1 = links.new(image_node.outputs[0], converter.inputs[1])
    link2 = links.new(layer_node.outputs[0], converter.inputs[2])
    link3 = links.new(converter.outputs[0], comp_node.inputs[0])


def prepare_camera(img_name, focal=21):
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
#    bpy.data.objects.remove(bpy.data.objects["Light"],do_unlink=True)
    if bpy.data.objects.get("Sun") is not None:
        bpy.data.objects.remove(bpy.data.objects["Sun"],do_unlink=True)
        
    bpy.ops.object.light_add(type="SUN")
    light_ob = bpy.context.object
    light_ob.location = location
    light_ob.rotation_euler = (rotation[0]*3.1416/180, rotation[1]*3.1416/180, rotation[2]*3.1416/180)
    light = light_ob.data
    light.energy = energy
    light.color = color
    

def render(resolution_x, resolution_y, path):
    bpy.context.scene.render.resolution_x = resolution_x
    bpy.context.scene.render.resolution_y = resolution_y
    bpy.context.scene.render.filepath = path
    bpy.context.scene.render.film_transparent = True
    bpy.ops.render.render(write_still = True)


def prepare_ground(location=(0,0,0), rotation= (3.1416/2,0,0), size=30):
#    objs = bpy.data.objects
    if bpy.data.objects.get("Plane") is not None:
        bpy.data.objects.remove(bpy.data.objects["Plane"],do_unlink=True)

    ground = bpy.ops.mesh.primitive_plane_add(size=size, enter_editmode=False, align='WORLD', location=location, rotation=rotation)

def place_object(location, rotation, obj_path):
    # TODO: set location and rotation of the object we want to place, then it will place the object at that pose.
    pass

def import_scene(path):
    # TODO: import 3D scene, I think it might be better to call pcl_visualizer 
    pass

def main():
    img_path = "I://Dense-Monocular-3D-Mapping-for-AR//ar_pipeline//city1.png"
    img = bpy.data.images.load(img_path)
    img_name = img_path.split("/")[-1]
    
    prepare_ground(location=(0,0.15,0.0))
    
    prepare_camera(img_name, 21)
    
    prepare_sun_light(location=(0,-1.8,0),rotation=(173,41.4,127), energy = 10)
    
    create_shadowcatecher("shadow_catcher")
    
    create_compositor(img_name)
    
    catcher = bpy.data.objects['Plane']
    
    assign_material(catcher, "shadow_catcher")
    
    path = 'C://Users//Lenovo//Desktop//img.jpg'
    render(1241, 376, path)
    
if __name__ == '__main__':
    main()