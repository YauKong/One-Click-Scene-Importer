The documentation and installation guide is here:

https://fish-resistance-484.notion.site/One-Click-Scene-Importer-V0-1-f90e033ef88d42caa17dfbb0cc7d8182

please follow the instruction within.

For demonstration purpose, you can use the Export_Testing_Folder as the import folder.

""""""""""""""""""
M_Master is the material I build to demonstrate how to pair the material parameter name.
You can abjust it to gain the best effect or write your own Material.
""""""""""""""""""
______________________________________

In case it didn't work,
1. Copy and Paste the One_Click_Importer_UI.uasset file into your unreal project, under the “Content” folder.
2. Open your Unreal Project and enabled the Python Editor Script Plugin. (Edit → Plugins)
3. Paste the “Python” folder comes with the plugin into the unreal project folder. Make sure it is under the “Content” folder.
4. Within the project setting, add an additional path for python plugin, make sure the path is the “Python” folder you just pasted in. 
(Edit → Project Setting → Plugins-Python) This is important or the plugin will not function as it can’t find the Python scripts.
5. After the last step, it will ask you for a restart, do it.
6. Go for the One_Click_Importer_UI under the “Content” Folder, you should see a Editor Utility Widget object, right click and click “Run Editor Utility Widget”
7. Done! Start to use the one-click importer! 