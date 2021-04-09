#!/usr/bin/env python3

import docker

def refresh_container(client, containers_names):

    failed = []
    for cname in containers_names:
        try:
            ct = client.containers.get(cname)
            ct.restart()
        except docker.errors.NotFound:
            failed = [*failed, cname]
    return failed

if __name__ == '__main__':
    client = docker.from_env()
    failed = refresh_container(client, ['some-mysql', 'some-postgres'])
    print(failed)