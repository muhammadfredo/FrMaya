'''
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 05 Mei 2018
Purpose      :

'''

import os
import shutil

import pymel.core as pm

def uninstall(*args, **kwargs):
    if kwargs:
        if kwargs.get('frmaya'):
            # Maya user script path
            usd = pm.internalVar( usd = True )
            # FrMaya script folder path
            script_folder = os.path.join( usd, 'FrMaya' )

            if os.path.exists(script_folder):
                shutil.rmtree( script_folder, ignore_errors=True)

            # userSetup.py path
            file_path = os.path.join(usd, 'userSetup.py')

            if os.path.exists(file_path):
                os.remove(file_path)
