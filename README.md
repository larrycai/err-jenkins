# err-jenkins - Jenkins plugin for Err

[![Build Status](https://travis-ci.org/Djiit/err-jenkins.svg?branch=master)](https://travis-ci.org/Djiit/err-jenkins)

Err-jenkins is a plugin for [err](https://github.com/gbin/err) that allows you to interact with [Jenkins](http://jenkins-ci.org), a continuous integration tool.

Note: This is a python3 compatible fork of https://github.com/benvd/err-jenkins

## Features

* Search / List available jobs.
* List parameters for a given job.
* Build jobs with or without parameters.
* Support AUTOINSTALL_DEPS thanks to the `requirements.txt` file.

Have an idea ? Open an [issue](https://github.com/Djiit/err-jenkins/issues) or send me a [Pull Request](https://github.com/Djiit/err-jenkins/pulls).

## Requirements

This plugin depends on the Python Jenkins:

```bash
pip install python-jenkins
```

## Installation

As admin of an err chatbot, send the following command over XMPP:

```
!install git://github.com/Djiit/err-jenkins.git
```

Then use `!help JenkinsBot` to see the available commands and their explanation.

## Configuration

You can set some default configuration values in your Errbot's `config.py`:

```python
JENKINS_URL = 'http://jenkins.example.com'  # Must begins with 'http' or 'https'.
JENKINS_USERNAME = 'myuser'  # Make sure Jenkins ACL is configured.
JENKINS_PASSWORD = 'mypassword'  # Use a password or token.
```

If left undefined, you will have to send configuration commands through chat message to this plugins as in :

```
!config JenkinsBot {'URL': 'http://jenkins.example.com', 'USERNAME': 'myuser', 'PASSWORD': 'mypassword'}
```
