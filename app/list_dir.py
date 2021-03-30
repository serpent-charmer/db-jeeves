import os
from os.path import isfile, isdir
from . import langs

def map_lang_dir(lang, path):
    if lang == langs.PY:
        return os.path.join(path, 'app')
    else:
        return path

def list_dir(path='.'):
    owd = path
    rs = {'title': os.path.basename(
        owd), 'key' : owd, 'expanded' : 'true', 'folder': 'true', 'children': dir_structure(owd)}
    return [rs]


def dir_structure(path='.'):
    rs = []
    if(os.path.exists(path)):
        for f in sorted(os.listdir(path)):
            pf = os.path.join(path, f)
            if(isfile(pf)):
                rs.append(dict({'title': f, 'key': pf}))
            else:
                rs.append(
                    dict({'title': f, 'key' : pf, 'expanded': 'true', 'folder': 'true', 'children': dir_structure(pf)}))
    return rs

