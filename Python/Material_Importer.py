import os
import unreal
import re


def log(message):
    unreal.log(message)
    pass


def scan_import_folder(import_folder_path):

    if not os.path.isdir(import_folder_path):
        log(f"Import folder not found at {import_folder_path}")
        return

    # Instancing an Asset tool for the following process.

    log("Created Asset import data.")
    # Destination folder that will contain all the new material instances.
    plugin_destination_path = '/Game/OC_Scene_Importer'
    set_folder(plugin_destination_path)
    log(f"Set the project folder at {plugin_destination_path}")

    # Build up folder to contain imported meshes.
    mesh_destination_path = f'{plugin_destination_path}/SI_Mesh'

    set_folder(mesh_destination_path)
    log(f"Set the mesh folder at {mesh_destination_path}")

    # Build up folder to contain imported Material.
    material_destination_path = f'{plugin_destination_path}/SI_Material'

    set_folder(material_destination_path)
    log(f"Set the material folder at {material_destination_path}")

    # Scan all the mesh and texture thats in the import folder.



    return  mesh_destination_path, material_destination_path


def import_mesh(mesh_files,
                import_folder_path, 
                destination_path):
    asset_tool = unreal.AssetToolsHelpers.get_asset_tools()
    asset_mesh_import_tasks = []
    imported_mesh = mesh_files
    mesh_path = []

    for mesh in imported_mesh:

        current_task = unreal.AssetImportTask()
        import_path = os.path.join(import_folder_path, mesh)

        current_task.filename = import_path
        current_task.destination_path = destination_path
        current_task.automated = True
        current_task.save = True

        options = get_import_options(mesh)
        if options:
            current_task.options = options

        current_file_path = f'{destination_path}/{mesh}'
        asset_mesh_import_tasks.append(current_task)
        mesh_path.append(current_file_path)

    asset_tool.import_asset_tasks(asset_mesh_import_tasks)
    return mesh_path


def create_material_instance(master_material_path,
                             material_instance_name,
                             material_instance_destination):
    
    # Instancing an Asset tool for the following process.
    asset_tool = unreal.AssetToolsHelpers.get_asset_tools()
    material_factory = unreal.MaterialInstanceConstantFactoryNew()

    # Load the master material
    master_material = unreal.EditorAssetLibrary.load_asset(
        master_material_path)
    if not master_material:
        log(f"Master material not found at {master_material_path}")
        return None
    
    # check if the material instance already existed
    if unreal.EditorAssetLibrary.does_asset_exist(f'{material_instance_destination}/{material_instance_name}'):
        
        # Return the material instance path and the material instance
        material_instance_path = f'{material_instance_destination}/{material_instance_name}'
        material_instance = unreal.EditorAssetLibrary.load_asset(
            material_instance_path)
        
        log(f"Material instance{material_instance_name} already existed at {material_instance_destination}")
        return material_instance_path, material_instance
    else:
        
        # Create a new material instance
        material_instance_path = f'{material_instance_destination}/{material_instance_name}'
        material_instance = asset_tool.create_asset(
            material_instance_name,
            material_instance_destination,
            unreal.MaterialInstanceConstant,
            material_factory)
        material_instance.set_editor_property('Parent', master_material)
        unreal.EditorAssetLibrary.save_loaded_asset(material_instance)
        log(f"Created {material_instance_name} at {material_instance_destination}")
        return material_instance_path, material_instance


def import_textures(mesh_files,
                                 texture_files,
                                 material_destination_path,
                                 texture_type):
    
    # Instancing an Asset tool for the following process.
    asset_tool = unreal.AssetToolsHelpers.get_asset_tools()
    # Build up folder to contain imported textures.
    texture_destination_path = f'{material_destination_path}/Textures'
    for mesh in mesh_files:
        mesh_name = mesh.split('.')[0]
        
        # Initailizing an Asset Import Task array for textures of the current mesh.
        asset_texture_import_tasks = []
        for texture in texture_files:

            # Get the texture name without the extension
            texture_base_name = os.path.basename(texture.split(".")[0])

            # Only put the texture that match the mesh name into the dictionary
            if mesh_name in texture_base_name:
                texture_set_name = re.sub(f'{mesh_name}_', '', texture_base_name)
                texture_format = texture_set_name.split('_')[-1]
                texture_set_name = re.sub(
                    f'_{texture_format}', '', texture_set_name)

                task = unreal.AssetImportTask()
                task.filename = texture
                task.destination_name = f'{mesh_name}_{texture_set_name}_{texture_format}'

                task.destination_path = f'{texture_destination_path}/{texture_set_name}'
                task.automated = True
                task.save = True
                current_asset_path = f'{task.destination_path}/{texture_set_name}/{task.destination_name}'

                # Check if the texture already existed in the destination folder
                if not unreal.EditorAssetLibrary.does_asset_exist(current_asset_path):
                    # Check if the task is already in the import task list
                    if task not in asset_texture_import_tasks:
                        asset_texture_import_tasks.append(task)
                        log(f"Created texture import task for {texture_set_name} - {texture_format}")
                else:
                    continue
            else:
                continue     
        if len(asset_texture_import_tasks) > 0:
            log(len(asset_texture_import_tasks))
            asset_tool.import_asset_tasks(asset_texture_import_tasks)


    return texture_destination_path


def orginize_texture(mesh_files, texture_type, texture_destination_path):
    all_texture_maps = {}
    for mesh in mesh_files:
        # Get the mesh name without the extension
        # UA = Unreal Asset
        UA_mesh_name = mesh.split(".")[0]
        # Create a dictionary to store the texture map if the mesh name is not in the dictionary
        if UA_mesh_name not in all_texture_maps:
            all_texture_maps[UA_mesh_name] = {}
        
        for texture in unreal.EditorAssetLibrary.list_assets(
            texture_destination_path, recursive=True):
            UA_texture_base_name = texture.split(".")[1]
            
            # Only put the texture that match the mesh name into the dictionary
            if UA_mesh_name in UA_texture_base_name:
                # Get the texture name without the extension
                UA_texture_set_name = re.sub(
                    f'{UA_mesh_name}_', '', UA_texture_base_name)
                # Get the texture format
                UA_texture_format = UA_texture_set_name.split('_')[-1]
                # Remove the texture format from the texture name
                UA_texture_set_name = re.sub(
                    f'_{UA_texture_format}', '', UA_texture_set_name)
                
                # Create a dictionary to store the texture format if the texture set name is not in the dictionary
                if UA_texture_set_name not in all_texture_maps[UA_mesh_name]:
                    all_texture_maps[UA_mesh_name][UA_texture_set_name] = {}

                for types in texture_type:
                    UA_texture_format = UA_texture_format.replace(" ", "")
                    UA_texture_format = UA_texture_format.replace("_", "")
                    types = types.replace(" ", "")
                    types = types.replace("_", "")
                    if types in UA_texture_format:
                        all_texture_maps[UA_mesh_name][UA_texture_set_name][UA_texture_format] = texture

    return all_texture_maps


def set_material_instance(all_texture_maps,
                          mesh_path, 
                          master_material_path, 
                          material_destination_path,
                          auto_assign_material):
    material_tool = unreal.MaterialEditingLibrary
    material_instance_sets = {}
    for mesh_name, mesh_map in all_texture_maps.items():
        for texture_set_name in mesh_map.keys():
            material_instance_name = f'MI_{texture_set_name}'
            
            material_instance_destination = f'{material_destination_path}/Material_Instance'
            MI_path, material_instance = create_material_instance(master_material_path,
                                                                  material_instance_name,
                                                                  material_instance_destination)
            material_instance_sets[material_instance_name] = MI_path
        
            for parameter, texture_path in all_texture_maps[mesh_name][texture_set_name].items():
                
                texture_package_name = texture_path.split(".")[0]
                texture = unreal.EditorAssetLibrary.load_asset(
                    texture_package_name)
                if texture:
                    
                    material_tool.set_material_instance_texture_parameter_value(
                        material_instance, parameter, texture)

                else:
                    log('Object texture invalid')
            #material_instance_sets[material_instance_name] = MI_path
        # log(f'Habibi: {material_instance_sets}')
    

    # Auto Assign Material to the mesh
    if auto_assign_material:
        for meshs in mesh_path:
            mesh_package_name = meshs.split(".")[0]
            static_mesh = unreal.EditorAssetLibrary.load_asset(mesh_package_name)
            static_mesh_component = unreal.StaticMeshComponent()
            static_mesh_component.set_static_mesh(static_mesh)
            material_slot_names = unreal.StaticMeshComponent.get_material_slot_names(
                static_mesh_component)
            mesh_material_match = {}

            # Create a dictionary to store the material index and the material slot name
            for material_slot_name in material_slot_names:
                material_index = unreal.StaticMeshComponent.get_material_index(
                    static_mesh_component, material_slot_name)
                mesh_material_match[material_index] = material_slot_name
                # log(f"The Current material slot is : {material_slot_name}[{material_index}]")
                for mi_name, mi_path in material_instance_sets.items():
                    material_slot_name_str = str(material_slot_name)

                    if material_slot_name_str in mi_name:
                        material_instance = unreal.EditorAssetLibrary.load_asset(
                            mi_path)
                        log(f"Material instance {mi_name} found")
                        static_mesh.set_material(material_index, material_instance)
                        log(f"Set material instance {mi_name} to the mesh {static_mesh.get_name()}")
                    else:
                        continue 
    return material_instance_destination


def get_import_options(file_name):
    # This function will be called by the import_mesh function
    # this function will be called by the import_and_set_textures function
    if ".fbx" in file_name:
        options = unreal.FbxImportUI()
        options.import_mesh = True
        options.import_as_skeletal = False
        # set the import options of combine meshes to ture

        options.static_mesh_import_data.combine_meshes = True
        options.static_mesh_import_data.auto_generate_collision = True
        options.static_mesh_import_data.generate_lightmap_u_vs = True
        options.import_animations = False
        options.import_materials = False
        options.import_textures = True

    elif ".obj" in file_name:
        options = unreal.FbxImportUI()
        options.is_obj_import = True
        options.import_materials = True
        options.import_textures = True
    elif ".usd" in file_name:
        # options = unreal.UsdStageImportOptions()
        # USD format is not supported yet.
        return None
    else:
        # If the file is a texture, return None
        # No need to set the import options for texture.
        file_extension = os.path.splitext(file_name)[1]
        log(f'Faild to get import option or file type{file_extension} invalid')
        return None
    return options


def scan_mesh_texture(import_folder_path, mesh_type, texture_type):
    """
    Scan the import_folder_path and find all the mesh that match
    the given mesh_type (Example: FBX)

    """
    mesh_files = []
    texture_files = []
    # Categories the mesh file by the mesh format
    for file in os.listdir(import_folder_path):
        for fmt in mesh_type:
            if file.endswith(fmt):
                mesh_files.append(file)
        for fmt in texture_type:
            if fmt in file:
                full_path = os.path.join(import_folder_path, file)
                texture_files.append(full_path)

    return mesh_files, texture_files


def set_folder(destination_path):
    if not unreal.EditorAssetLibrary.does_directory_exist(destination_path):
        unreal.EditorAssetLibrary.make_directory(destination_path)
        log(f"Created target folder at{destination_path}")
    else:
        log(f"The destination folder had already existed.")


def execute(import_folder_path,
            master_material_path,
            auto_assign_material):
    """
    This is the execute function that will be called by the Unreal Engine
    """
    import_folder_path = import_folder_path
    master_material_path = master_material_path

    # Define the mesh type that the script will recognize
    mesh_type = [".fbx", ".obj", ".usd"]
    log(f"The current recognizable 3D file formats are: ")
    for mesh in mesh_type:
        print(f"3D Format: {mesh}")
    
    # Define the texture type that the script will recognize
    texture_type = ["BaseColor", "Normal", "ARM", "Height", "Emissive"]
    log(f"The current recognizable Texture formats are: ")
    for texture in texture_type:
        print(f"3D Format: {texture}")

    if os.path.isdir(import_folder_path):

        mesh_destination_path, material_destination_path = scan_import_folder(
            import_folder_path)
        
        mesh_files, texture_files = scan_mesh_texture(import_folder_path,
                                                      mesh_type,
                                                      texture_type)
        
        mesh_path = import_mesh(mesh_files, 
                                import_folder_path, 
                                mesh_destination_path)
        
        texture_destination_path = import_textures(mesh_files,
                                                   texture_files,
                                                   material_destination_path,
                                                   texture_type)
        
        all_texture_maps = orginize_texture(mesh_files, 
                                            texture_type, 
                                            texture_destination_path)

        material_instance_destination =set_material_instance(all_texture_maps,
                                                             mesh_path,
                                                             master_material_path,
                                                             material_destination_path,
                                                             auto_assign_material)
        return material_instance_destination
    else:
        log(f"{import_folder_path} path invalid.")

if __name__ == "__main__":
    execute()

