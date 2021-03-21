import os
from os.path import isfile, isdir


def list_dir(path='.'):
    owd = path
    rs = {'title': os.path.basename(
        owd), 'key' : owd, 'expanded' : 'true', 'folder': 'true', 'children': dir_structure(owd)}
    return [rs]


def dir_structure(path='.'):
    rs = []
    py_path = os.path.join(path, 'app')
    if(os.path.exists(py_path)):
        path = py_path
    if(os.path.exists(path)):
        for f in sorted(os.listdir(path)):
            pf = os.path.join(path, f)
            if(isfile(pf)):
                rs.append(dict({'title': f, 'key': pf}))
            else:
                rs.append(
                    dict({'title': f, 'key' : pf, 'expanded': 'true', 'folder': 'true', 'children': dir_structure(pf)}))
    return rs

