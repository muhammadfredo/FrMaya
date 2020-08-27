'''
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 12 Feb 2018
Purpose      :

'''

# install new FrMaya Core
# install new FrMaya 3rd party lib
# update FrMaya
# update custom core or 3rd party lib separately

# main instal frmaya
##
import os
import shutil

import pymel.core as pm
import FrMaya
import baseUninstall


def install(*args, **kwargs):
    if kwargs:
        # Maya user script path
        usd = pm.internalVar(usd=True)
        if kwargs.get('source') and kwargs.get('local'):
            # uninstall frmaya if any
            baseUninstall.uninstall(frmaya=True)

            # FrMaya script folder path
            script_folder = os.path.join(usd, 'FrMaya')

            # copy frmaya to usd
            shutil.copytree( kwargs.get('source'), script_folder )

            # userSetup.py path
            file_path = os.path.join(usd, 'userSetup.py')

            script_file = ''

            # check if userSetup exist
            if os.path.exists(file_path):
                # TODO: append FrMaya userSetup to existing userSetup
                pass

            script_file += 'import FrMaya\n'
            script_file += 'FrMaya.startup()\n'

            with open(file_path, 'w') as ss:
                ss.write(script_file)

        if kwargs.get('source') and kwargs.get('remote'):
            # uninstall frmaya if any
            baseUninstall.uninstall( frmaya = True )

            file_path = os.path.join(usd, 'userSetup.py')

            with open(file_path, 'w') as ss:
                ss.write("import sys\n")
                ss.write("sys.path.append(r'{0}')\n".format(os.path.dirname(kwargs.get('source'))))
                ss.write("import FrMaya\n")
                ss.write("FrMaya.startup()\n")

        return True
    else:
        print 'please specify keyword argument'
        return False




