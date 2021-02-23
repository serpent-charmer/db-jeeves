import os
from os.path import isfile, isdir


def list_dir(path='.'):
    owd = path
    rs = {'title': os.path.basename(
        owd), 'folder': 'true', 'children': dir_structure(owd)}
    return [rs]


def dir_structure(path='.'):
    rs = []
    if(os.path.exists(path)):
        for f in os.listdir(path):
            pf = os.path.join(path, f)
            if(isfile(pf)):
                rs.append(dict({'title': f, 'key': pf}))
            else:
                rs.append(
                    dict({'title': f, 'folder': 'true', 'children': dir_structure(pf)}))
    return rs

