from abc import ABC, abstractmethod

class SlaveInterface:

    @abstractmethod
    def slave_create():
        pass

    @abstractmethod
    def slave_delete():
        pass

    def slave_download(target):
        if os.path.isfile(slave_jar):
            os.remove(slave_jar)

        loader = urllib.URLopener()
        loader.retrieve(slave_jar_url, slave_jar)

    def slave_run(slave_jar, jnlp_url):
        params = [ 'java', '-jar', slave_jar, '-jnlpUrl', jnlp_url ]
        if os.environ['JENKINS_SLAVE_ADDRESS'] != '':
            params.extend([ '-connectTo', os.environ['JENKINS_SLAVE_ADDRESS' ] ])

        if os.environ['SLAVE_SECRET'] == '':
            params.extend([ '-jnlpCredentials', os.environ['JENKINS_USER'] + ':' + os.environ['JENKINS_PASS'] ])
        else:
            params.extend([ '-secret', os.environ['SLAVE_SECRET'] ])
        return subprocess.Popen(params, stdout=subprocess.PIPE)
