# JENKINS DOCKER EASY SETUP
Quick & easy configuration to run Jenkins on docker.
Repository based on the work of [CodeMazeBlog](https://github.com/CodeMazeBlog) [docker-series](https://github.com/CodeMazeBlog/docker-series)


## Usage:

First clone the repository to your local machine:

`git clone git@github.com:adzarei/easy-jenkins-docker.git`

Then spin up the containers with docker-compose:

`docker-compose up --build`

You can set the number of Jenkins agents with docker-compose' flag scale:

`docker-compose up --build --scale jenkins-agent=2`
