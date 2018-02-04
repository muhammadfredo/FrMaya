'''
####################################################################################
####################################################################################
## SCRIPT HEADER ##
# Created By            : Muhammad Fredo Syahrul Alam
# Email                 : muhammadfredo@gmail.com
# Start Date            : 16 December, 2016

# Purpose: 
# Bugs: 
# History: 
####################################################################################
####################################################################################
'''

def renameSkin( ns ):
    print ns
    #get skincluster from object
    for o in ns:
        history = mc.listHistory( o, pdo = True, il = 1 )
        if history != None:
            for x in history:
                if mc.nodeType( x ) == "skinCluster":
                    nmspce = o.split( ":" )
                    if len(nmspce) > 1:
                        mc.rename( x, nmspce[1].replace("MSH","SKN") )
                    else:
                        mc.rename( x, nmspce[0].replace("MSH","SKN") )

renameSkin( mc.ls("*:*MSH") + mc.ls("*MSH") )