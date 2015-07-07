'''
This modules contains the structure of ICE's script menu that is drawn inside Maya
'''

import pymel.core as pc
from command import command
import mayaStartup
reload(mayaStartup)
import json, os, sys, random
from site import addsitedir as asd
op = os.path

menu_name = 'ICE_Menu'
#spice = ['Scripts']

def construct_menu(parent, structure = {}):

    for item in sorted(structure):
        value = structure[item]
        retired = value.get('_retire', False)
        if not retired:
            leaf = value.get('_leaf', False)
            kwargs = {'parent': parent,
                      'label': item,
                      'ann': value.get('_annotation', "")}

            if leaf:
                try:
                    call = Menu.call(call = value['_call'])
                except Exception as e:
                    def call(*args): print 'Nothing to call'
                    
                kwargs['c'] = call
                
                pc.menuItem(**kwargs)

            else:

                kwargs['to'] = True
                construct_menu(pc.subMenuItem(**kwargs), value)

def create_menu(*args):
    
    reload(command)
    global Menu
    Menu = command.Menu
    menu_title = 'ICE Scripts' #%(random.choice(spice))
    gMainWindow = pc.mel.eval('$tmpVar = $gMainWindow')
    if pc.menu(menu_name, exists = True):
        pc.deleteUI(menu_name)
    menu = pc.menu(menu_name, parent = gMainWindow, label = menu_title,
                   to = True)

    with open(op.join(op.dirname(__file__), 'command', 'menu.json'), 'r') as f:
        menu_structure = json.load(f)

    construct_menu(menu, menu_structure)
    pc.menuItem(parent = menu, divider = True, to = True)
    # pc.menuItem(parent = menu,
    #             label = 'Search ..',
    #             command = lambda *arg: None,
    #             ann = 'Search the menu')
    pc.menuItem(parent = menu,
                label = 'Rebuild This Menu',
                command = create_menu,
                ann = 'This will reconstruct the entire menu')
    return menu



def startup():
    create_menu()
    mayaStartup.start()

startup()