import docker
import subprocess
import os


from uuid import uuid4
from distutils.dir_util import copy_tree, remove_tree


def copy_new_img(path, new_path):
    u_path = os.path.join('users', new_path)
    try:
        remove_tree(u_path)
    except:
        pass
    finally:
        copy_tree(os.path.join('images', path), u_path)
    return u_path


def copy_php_img(name):
    return 'php', copy_new_img('php-img', name)


def copy_py_img(name):
    return 'python', copy_new_img('py-img', name)


def copy_js_img(name):
    return 'javascript', copy_new_img('js-img', name)


def build_custom_img(path, name):

    client = docker.from_env()
    img = client.images.build(path=path, tag=name)
    #print(img)

    container_name = 'container-'+name

    try:
        container = client.containers.get(container_name)
        container.remove(force=True)
    except:
        pass

    container = client.containers.create(name,
                                         name=container_name,
                                         extra_hosts={"mysql-db": '10.11.3.3'},
                                         network='db_network', detach=True, ports={8000: None})

    container.start()
    container.reload()
#	print('Container ports', container.ports)

    client.close()

    return container


if __name__ == '__main__':
    nm = 'new-user-312315fwefg3453'
    nm_path = 'path-' + nm
    copy_new_img('php-img', nm_path)

    container = build_custom_img(nm_path, nm)
    print(container.ports['8000/tcp'][0]['HostPort'])

    # print(docker.from_env().images.list())
    print(docker.from_env().containers.list())
