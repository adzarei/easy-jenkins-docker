# from abc import ABCMeta, abstractmethod
import os
import urllib
import subprocess
import requests

class SlaveBase():
    '''Base Class for slave objects'''
    # __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @property
    def slave_jar(self):
        return '/var/lib/jenkins/slave.jar'

    @property
    def jnlp_url(self):
        raise NotImplementedError()

    @property
    def jenkins_url(self):
        raise NotImplementedError()

    @property
    def slave_jar_url(self):
        raise NotImplementedError()

    @property
    def slave_address(self):
        raise NotImplementedError()

    @property
    def slave_secret(self):
        raise NotImplementedError()

    @property
    def jenkins_user(self):
        raise NotImplementedError()

    @property
    def jenkins_password(self):
        raise NotImplementedError()

    # @abstractmethod
    def slave_create(self, node_name, working_dir, executors, labels):
        raise NotImplementedError()

    # @abstractmethod
    def slave_delete(self, node_name):
        raise NotImplementedError()

    def master_ready(self):
        try:
            r = requests.head(self.slave_jar_url, verify=False, timeout=None)
            return r.status_code == requests.codes.ok
        except:
            return False

    def slave_download(self):
        if os.path.isfile(self.slave_jar):
            os.remove(self.slave_jar)

        loader = urllib.URLopener()
        loader.retrieve(self.slave_jar_url, self.slave_jar)

    def slave_run(self):
        params = [ 'java', '-jar', self.slave_jar, '-jnlpUrl', self.jnlp_url ]
        if self.slave_address != '':
            params.extend([ '-connectTo', self.slave_address ])

        if self.slave_secret == '':
            params.extend([ '-jnlpCredentials', self.jenkins_user + ':' + self.jenkins_password ])
        else:
            params.extend([ '-secret', self.slave_secret ])
        return subprocess.Popen(params, stdout=subprocess.PIPE)
