import os
import maya.cmds as mc
import ctypes
from ctypes.wintypes import MAX_PATH

plugin_path = 'R:/Python_Scripts/plugins/Sunday'
plugin_name = 'SundayPluginPublic'


def add_path():
    mayapp = os.environ['MAYA_PLUG_IN_PATH']
    mayapp = mayapp.split(';')
    if plugin_path not in mayapp:
        mayapp.append(plugin_path)
        os.environ['MAYA_PLUG_IN_PATH']=';'.join(mayapp)


def add_path_env():
    env_file_path = os.path.join(docFolder(), 'maya', 'Maya.env')
    myline = "MAYA_PLUG_IN_PATH=%s;%%MAYA_PLUG_IN_PATH%%" % plugin_path
    path_exists = False
    if os.path.exists(env_file_path):
        with open(env_file_path) as envfile:
            if myline in envfile.readlines():
                path_exists=True
    if not path_exists:
        with open(env_file_path, 'a') as envfile:
            envfile.writelines([myline])
        return True
    return False


def docFolder():
    dll = ctypes.windll.shell32
    buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
    if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
        return buf.value
    else:
        return os.path.join(os.environ['USERPROFILE'], 'Documents')

def load_plugin():
    mc.loadPlugin(plugin_name)


def install():
    add_path()
    add_path_env()
    load_plugin()

if __name__ == '__main__':
    install()


