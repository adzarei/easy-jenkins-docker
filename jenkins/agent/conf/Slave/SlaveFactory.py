from Slave.imp.PythonJenkinsSlave import PythonJenkinsSlave
from Slave.SlaveBase import SlaveBase


class SlaveFactory():

    def __init__ (self, jenkins_url ,jenkins_user, jenkins_password, slave_address='', slave_secret=''):
        self.jenkins_url = jenkins_url
        self.jenkins_user = jenkins_user
        self.jenkins_password = jenkins_password
        self.slave_address = slave_address
        self.slave_secret = slave_secret


    def get_slave(self, slave_type):
        if slave_type.upper() == 'PYTHON_JENKINS':
            return PythonJenkinsSlave(self.jenkins_url, self.jenkins_user, self.jenkins_password, slave_address=self.slave_address)
        else:
            raise NotImplementedError('Slave Type: ' + slave_type + " not implemented yet.")
