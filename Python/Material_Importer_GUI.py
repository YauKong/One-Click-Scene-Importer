import unreal
import os
import Material_Importer as Material_Importer



# Define a function to call the Material_Importer module
def call_material_importer(import_folder_path,
                            master_material_path,
                            auto_assign_material):
    material_instance_destination = Material_Importer.execute(import_folder_path, 
                                                            master_material_path,
                                                            auto_assign_material)
    return material_instance_destination


if Material_Importer:
    print("Material Importer is loaded")