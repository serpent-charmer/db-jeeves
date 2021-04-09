import docker
import subprocess
import os


from uuid import uuid4
from distutils.dir_util import copy_tree, remove_tree, create_tree
from . import mvars


def copy_new_img(path, new_path):
    u_path = os.path.join('users', new_path)
    i_path = os.path.join('images', path)
    try:
        remove_tree(u_path)
    except:
        pass
    finally:
        create_tree(u_path, os.listdir(i_path))
        copy_tree(i_path, u_path)
    return u_path


def copy_php_img(name):
    return 'php', copy_new_img('php-img', name)


def copy_py_img(name):
    return 'python', copy_new_img('py-img', name)


def copy_js_img(name):
    return 'javascript', copy_new_img('js-img', name)


def build_custom_img(path, name):

    client = docker.from_env()

    client.images.prune()
    client.containers.prune()

    client.images.build(path=path, tag=name, rm=True)

    container_name = 'container-'+name

    try:
        container = client.containers.get(container_name)
        container.remove(force=True)
    except:
        pass

    container = client.containers.create(name,
                                         name=container_name,
                                         extra_hosts={"mysql-db": mvars.MY_SQL_IP,
                                                      "pgsql-db": mvars.PG_SQL_IP},
                                         network='db_network',
                                         detach=True,
                                         ports={mvars.DEFAULT_PORT: None},
                                         environment=['DEFAULT_PORT=%d' % mvars.DEFAULT_PORT, 'DB_LOGIN=%s' % name, 'DB_PWD=abc', 'DB_NAME=%s' % (name+"db")])

    container.start()
    container.reload()

    client.close()

    return container


def get_container_logs(name):
    container_name = 'container-'+name

    client = docker.from_env()

    container = client.containers.get(container_name)

    client.close()

    return container.logs().decode(encoding='utf-8')


def get_container_port(container):
    return container.ports['%d/tcp' % mvars.DEFAULT_PORT][0]['HostPort']


if __name__ == '__main__':
    nm = 'new-user-312315fwefg3453'
    nm_path = 'path-' + nm
    copy_new_img('php-img', nm_path)

    container = build_custom_img(nm_path, nm)
    print(container.ports['8000/tcp'][0]['HostPort'])

    # print(docker.from_env().images.list())
    print(docker.from_env().containers.list())
