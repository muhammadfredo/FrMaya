"""
####################################################################################
####################################################################################
## SCRIPT HEADER ##
# Created By             : Muhammad Fredo
# Email                      : muhammadfredo@gmail.com
# Start Date               : 12 Sep, 2017
# Last Modified Date       :
# Purpose:
# Bugs:
# History:
# Note:
####################################################################################
####################################################################################
"""
import os

import MainTool as tool
import FrMaya

reload(tool)


def show(source_path = '', install_btn = False, update_btn = False, remove_btn = False):
    # Show tool window
    the_tool = tool.MainGUI()

    if source_path:
        the_tool.set_source_path(source_path)
    elif not source_path:
        the_tool.set_source_path(os.path.dirname(FrMaya.basedir()))

    the_tool.ui.install_btn.setEnabled(install_btn)
    the_tool.ui.update_btn.setEnabled(update_btn)
    the_tool.ui.remove_btn.setEnabled(remove_btn)

    the_tool.show()
