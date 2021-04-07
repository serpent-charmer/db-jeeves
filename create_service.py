#!/usr/bin/env python3

import os
if __name__ == '__main__':

    content = '''
    [Unit]
    Description=DBJeeves

    [Service]
    Environment=FLASK_ENV=production
    User=db_jeeves_user
    Group=webdev

    WorkingDirectory={0}
    ExecStart={0}/run_gunicorn.sh
    Restart=always

    [Install]
    WantedBy=multi-user.target
    '''


    with open('db_jeeves.service', 'w+') as f:
        f.write(content.format(os.getcwd()))