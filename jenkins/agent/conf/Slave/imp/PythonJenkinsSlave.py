# python-jenkins
# https://python-jenkins.readthedocs.io/en/latest/
import jenkins

from Slave.SlaveBase import SlaveBase

class PythonJenkinsSlave(SlaveBase):

    __url = ''
    __user = ''
    __password = ''
    __slave_name = ''
    __slave_secret =''
    __slave_address = ''
    __jenkins_master = None


    def __init__(self, jenkins_url, jenkins_user, jenkins_password, slave_address='', slave_secret=''):
        self.__url = jenkins_url
        self.__user = jenkins_user
        self.__password = jenkins_password
        self.__slave_secret = slave_secret
        self.__slave_address = slave_address

    @property
    def jenkins_url(self):
        return self.__url

    @property
    def slave_jar(self):
        return '/var/lib/jenkins/slave.jar'

    @property
    def jnlp_url(self):
        return self.jenkins_url + '/computer/' + self.__slave_name + '/slave-agent.jnlp'

    @property
    def slave_jar_url(self):
        return self.jenkins_url + '/jnlpJars/slave.jar'

    @property
    def slave_address(self):
        return self.__slave_address

    @property
    def slave_secret(self):
        return self.__slave_secret

    @property
    def jenkins_user(self):
        return self.__user

    @property
    def jenkins_password(self):
        return self.__password

    @property
    def jenkins_master(self):
        if self.__jenkins_master is not None:
            self.__jenkins_master
        else:
            if self.master_ready():
                return jenkins.Jenkins(self.jenkins_url, username=self.jenkins_user, password=self.jenkins_password)

            else:
                raise Exception('Master is not ready!')

    def slave_create(self, node_name, working_dir, executors, labels):
        self.__slave_name = node_name
        self.jenkins_master.create_node(node_name, remoteFS=working_dir, numExecutors=int(executors), labels=labels, launcher=jenkins.LAUNCHER_JNLP)

    def slave_delete(self, node_name):
        self.jenkins_master.delete_node(node_name)
