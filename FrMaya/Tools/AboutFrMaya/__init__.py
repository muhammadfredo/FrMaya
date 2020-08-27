'''
####################################################################################
####################################################################################
## SCRIPT HEADER ##
# Created By             : Muhammad Fredo Syahrul Alam
# Email                      : muhammadfredo@gmail.com
# Start Date               : 12 Sep, 2017
# Last Modified Date       : 
# Purpose: 
# Bugs: 
# History: 
# Note: 
####################################################################################
####################################################################################
'''
import MainTool as tool
import FrMaya
reload(tool)

def show(source_path = '', install_btn = False, update_btn = False, remove_btn = False):
    # Show tool window
    theTool = tool.MainGUI()

    if source_path:
        theTool.source_path = source_path
    elif not source_path:
        theTool.source_path = FrMaya.basedir()

    theTool.ui.install_btn.setEnabled( install_btn )
    theTool.ui.update_btn.setEnabled( update_btn )
    theTool.ui.remove_btn.setEnabled( remove_btn )

    theTool.show()