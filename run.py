#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

# --------------------------------------------
# Author: Thales Claro Pereira
# --------------------------------------------
import os
import sys
import socket
import argparse
import signal
import requests
import subprocess
from pathlib import Path


class Utilities(object):

    @staticmethod
    def jenkins_war_path():
        return os.path.join('bin', 'jenkins.war')

    @staticmethod
    def download_jenkins():

        if os.path.exists(Utilities.jenkins_war_path()):
            pass
        else:
            print('Downloading Jenkins war file, please wait...')
            os.mkdir('bin')
            filename = Path(Utilities.jenkins_war_path())
            url = 'http://mirrors.jenkins.io/war-stable/latest/jenkins.war'
            r = requests.get(url)
            filename.write_bytes(r.content)

            print('Download finished.')

    @staticmethod
    def port_check():
        addr = '127.0.0.1'
        port = 8080

        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    result = s.connect((addr, port))
                    if result == 0:
                        print(f'port {port} is open')
                    port = port +1
                except:
                    return port


class JenkinsManager(object):

    def __init__(self, name):
        self.name = name

    def setup(self):
        os.makedirs(self.instance_path())
        os.mkdir('run')
        os.mkdir('logs')

    def instance_path(self):
        return os.path.join('instances', self.name)

    def deploy(self):
        if os.path.exists(self.instance_path()):
            print(f'{self.name} already exists, aborting.')
            sys.exit(1)
        else:
            print(f'Deploying New jenkins master Server: {self.name}')
            self.setup()
            Utilities.download_jenkins()

        self.launch_and_watch()
        sys.exit(0)

    def remove(self):
        pass

    def status(self):
        pass

    def stop(self):
        pid_file = os.path.join(os.getcwd(), 'run', f'{self.name}.pid')
        c = int(Path(pid_file).read_text())
        print(os.getp(c))

    def launch_and_watch(self):
        port = Utilities.port_check()

        subprocess.Popen(
            'wrapper.sh', env=dict(
                **{
                    'PIDFILE': os.path.join(os.getcwd(), 'run', f'{self.name}.pid'),
                    'JENKINS_HOME': self.instance_path(),
                    'LOGFILE': os.path.join(os.getcwd(), 'logs', f'{self.name}.log'),
                    'PORT': f'{port}'
                }
            )
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Launch Jenkins instances when docker available')
    parser.add_argument('-i', '--instance', help='Instance name', required=True)
    parser.add_argument('-d', '--deploy', help='Deploy new Jenkins instace', action='store_true')
    parser.add_argument('-R', '--remove', help='Remove existing Jenkins instance', action='store_true')
    parser.add_argument('-S', '--stop', help='Remove existing Jenkins instance', action='store_true')
    parser.add_argument('-s', '--status', help='Jenkins status', action='store_true')
    args = parser.parse_args()

    manager = JenkinsManager(args.instance)

    if args.deploy:
        manager.deploy()
    elif args.remove:
        manager.remove()
    elif args.status:
        manager.status()
    elif args.stop:
        manager.stop()
    else:
        print('Option not available, use --help instead.')

