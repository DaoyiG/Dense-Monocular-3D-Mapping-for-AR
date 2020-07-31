import bpy

# Clear all nodes in a mat
def clear_material( material ):
    if material.node_tree:
        material.node_tree.links.clear()
        material.node_tree.nodes.clear()

materials = bpy.data.materials

def create_shadowcatecher(name):
    mat_name = name

    material = materials.get( mat_name )

    if not material:
        material = materials.new( mat_name )

    # We clear it as we'll define it completely
    clear_material( material )

    material.use_nodes = True

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

    diffuse2.inputs[0].default_value = ( 0,0,0,1)


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


create_shadowcatecher("shadow_catcher")
obj = bpy.data.objects['Plane']

#mat = bpy.data.materials["shader_catcher1"]
assign_material(obj, "shadow_catcher")

