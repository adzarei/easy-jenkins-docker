from Slave.SlaveFactory import SlaveFactory
import time
import os
import shutil

def main():
    process = None
    slave_name = os.environ['SLAVE_NAME'] if os.environ['SLAVE_NAME'] != '' else 'docker-slave-' + os.environ['HOSTNAME']

    slaveFactory = SlaveFactory(
        os.environ['JENKINS_URL'],
        os.environ['JENKINS_USER'],
        os.environ['JENKINS_PASS'],
        os.environ['JENKINS_SLAVE_ADDRESS'],
        os.environ['SLAVE_SECRET']
    )

    slave = slaveFactory.get_slave("PYTHON_JENKINS")

    # Wait for jenkins master to be ready:
    while not slave.master_ready():
        print("Master not ready yet, sleeping for 10sec!")
        time.sleep(10)

    print("Master is ready")

    slave.slave_download()
    print("Jenkins slave jar succesfully downloaded")

    # Move to working directory
    if os.environ['SLAVE_WORING_DIR']:
        os.setcwd(os.environ['SLAVE_WORING_DIR'])
        print("Change directory to: " + os.environ['SLAVE_WORING_DIR'])

    # Clean working directory.
    if os.environ['CLEAN_WORKING_DIR'] == 'true':
        clean_dir(os.getcwd())
        print("Cleaned up working directory.")

    # Create Jenkins Agent
    slave.slave_create(slave_name, os.getcwd(), os.environ['SLAVE_EXECUTORS'], os.environ['SLAVE_LABELS'])
    print('Created temporary Jenkins slave.')

    # Run slave JAR.
    process = slave.slave_run()
    print('Started Jenkins Agent with name "' + slave_name + '" and labels [' + os.environ['SLAVE_LABELS'] + '].')
    process.wait()

    #Gracefully close jankins agent.
    print('Jenkins Agent stopped.')
    if os.environ['SLAVE_NAME'] == '':
        slave_delete(slave_name)
        print('Removed temporary Jenkins Agent.')


def clean_dir(dir):
    for root, dirs, files in os.walk(dir):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))



if __name__ == "__main__":
    main()
