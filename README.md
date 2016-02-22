Note: This is a python3 compatible fork of https://github.com/benvd/err-jenkins

# err-jenkins - Jenkins plugin for Err

Err-jenkins is a plugin for [err](https://github.com/gbin/err) that allows you to interact with [Jenkins](http://jenkins-ci.org), a continuous integration tool.

For now it only allows you to list (and search) all the jobs, and get an overview of running jobs.

## Requirements

This plugin depends on the Python Jenkins:

    pip install python-jenkins

## Installation

As admin of an err chatbot, send the following command over XMPP:

    !install git://github.com/Djiit/err-jenkins.git

Then use `!help` to see the available commands and their explanation.

Before you can use the plugin, you have to add the following three variables to `config.py`:

    JENKINS_URL = 'http://jenkins.example.com'  # Must begins with 'http' or 'https'.
    JENKINS_USERNAME = 'myuser'  # Make sure Jenkins ACL is activated.
    JENKINS_PASSWORD = 'mypassword'  # Use a password or token.
