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
import requests
import subprocess
from pathlib import Path
from configparser import ConfigParser


base_dir = os.path.dirname(os.path.abspath(__file__))


class Utilities(object):

    @staticmethod
    def jenkins_war_path():
        base_dir = Utilities.get('path', 'base')
        bin = Utilities.get('path', 'bin')
        war_file = Utilities.get('jenkins', 'war_file')
        return os.path.join(base_dir, bin, war_file)

    @staticmethod
    def download_jenkins():
        if os.path.exists(Utilities.jenkins_war_path()):
            pass
        else:
            print('Downloading Jenkins war file, please wait...')
            filename = Path(Utilities.jenkins_war_path())
            url = Utilities.get('jenkins', 'war_url')
            r = requests.get(url)
            filename.write_bytes(r.content)

    @staticmethod
    def port_check():
        ipaddr = Utilities.get('server', 'ipaddr')
        port = Utilities.get('server', 'base_port')
        port = int(port)
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    result = s.connect((ipaddr, port))
                    if result == 0:
                        print(f'port {port} is open')
                    port = port + 1

                except:
                    return port

    @staticmethod
    def get(section, key):
        config_file = 'config.ini'
        config_file_path = os.path.join(base_dir, config_file)

        if os.path.exists(config_file_path):
            try:
                config = ConfigParser()
                config.read(config_file_path)
                return config.get(section, key)
            except KeyError:
                print(f'Section: {section} or Key: {key} not found.')
                sys.exit(1)
        else:
            print('Error : Configuration file not found')
            print(f'Please check if {base_dir}/{config_file} exsits')
            sys.exit(1)

    @staticmethod
    def create_dir(dirname):
        full_path = os.path.join(base_dir, dirname)
        if not os.path.exists(full_path):
            os.makedirs(full_path)


class JenkinsManager(object):

    def __init__(self, name):
        self.name = name

    def setup(self):
        for i in [self.log_path(), self.bin_path(), self.pid_path(), self.instance_path()]:
            Utilities.create_dir(i)

    def log_path(self):
        base_dir = Utilities.get('path', 'base')
        log_dir = Utilities.get('path', 'logdir')
        return os.path.join(base_dir, log_dir)

    def bin_path(self):
        base_dir = Utilities.get('path', 'base')
        bin_dir = Utilities.get('path', 'bin')
        return os.path.join(base_dir, bin_dir)

    def pid_path(self):
        base_dir = Utilities.get('path', 'base')
        pid_dir = Utilities.get('path', 'pid_store')
        return os.path.join(base_dir, pid_dir)

    def instance_path(self):
        base = Utilities.get('path', 'base')
        instances = Utilities.get('path', 'instances')
        return os.path.join(base, instances, self.name)

    def deploy(self):
        if os.path.exists(self.instance_path()):
            print(f'{self.name} already exists, aborting.')
            sys.exit(1)
        else:
            print(f'Deploying New jenkins master Server: {self.name}')
            self.setup()
            Utilities.download_jenkins()
            self.start_jenkins()
            sys.exit(0)

    def remove(self):
        pass

    def status(self):
        pass

    def stop(self):
        pass

    def backup(self):
        pass

    def start_jenkins(self):
        port = Utilities.port_check()
        delay = Utilities.get('internal', 'delay')
        subprocess.Popen(
            'wrapper.sh', env=dict(
                **{'JENKINS_WAR_FILE': Utilities.jenkins_war_path() ,
                    'PIDFILE': os.path.join(self.log_path(), f'{self.name}.pid'),
                    'NAME': self.name,
                    'JENKINS_HOME': self.instance_path(),
                    'LOGFILE': os.path.join(self.log_path(), self.name),
                    'PORT': f'{port}',
                    'DELAY': f'{delay}'
                }
            )
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Launch Jenkins instances when docker available')
    parser.add_argument('-i', '--instance', help='Instance name', required=True)
    parser.add_argument('-d', '--deploy', help='Deploy new Jenkins instace', action='store_true')
    parser.add_argument('-R', '--remove', help='Remove existing Jenkins instance', action='store_true')
    parser.add_argument('-S', '--stop', help='Stop Jenkins instance', action='store_true')
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

