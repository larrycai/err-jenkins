# coding: utf-8
from errbot.backends.test import testbot

import jenkinsBot


class TestJenkinsBot(object):
    extra_plugin_dir = '.'

    # def test_jenkins_build_no_args(self, testbot):
    #     testbot.push_message('!jenkins build')
    #     assert ('What job would you like to build?'
    #             in testbot.pop_message())

    # def test_jenkins_build_shortcut_no_args(self, testbot):
    #     testbot.push_message('!build')
    #     assert ('What job would you like to build?'
    #             in testbot.pop_message())

    # def test_jenkins_param_no_args(self, testbot):
    #     testbot.push_message('!jenkins param')
    #     assert ('What Job would you like the parameters for?'
    #             in testbot.pop_message())


class TestJenkinsBotStaticMethods(object):

    def test_format_jobs_helper(self):
        jobs = [{'name': 'foo',
                 'fullname': 'foo bar',
                 'url': 'http://jenkins.example.com/job/foo/'}]
        result = jenkinsBot.JenkinsBot.format_jobs(jobs)
        assert result == 'foo (http://jenkins.example.com/job/foo/)'

    def test_format_jobs_helper_no_params(self):
        jobs = []
        result = jenkinsBot.JenkinsBot.format_jobs(jobs)
        assert result == 'No jobs found.'

    def test_format_params_helper(self):
        params = [{
            'defaultParameterValue': {'value': 'bar'},
            'description': 'foo bar baz',
            'name': 'FOO',
            'type': 'StringParameterDefinition'
        }]
        result = jenkinsBot.JenkinsBot.format_params(params)
        assert result == """Type: StringParameterDefinition
Description: foo bar baz
Default Value: bar
Parameter Name: FOO

"""

    def test_build_parameters_helper(self):
        params = ['FOO:bar', 'BAR:baz']
        result = jenkinsBot.JenkinsBot.build_parameters(params)
        assert result == {'FOO': 'bar', 'BAR': 'baz'}

    def test_build_parameters_helper_no_params(self):
        params = []
        result = jenkinsBot.JenkinsBot.build_parameters(params)
        assert result == {'': ''}

    def test_format_notification(self):
        body = {
            "name": "dummy",
            "url": "job/dummy/",
            "build": {
                "full_url": "http://jenkins.example.com/job/dummy/1/",
                "number": 1,
                "phase": "COMPLETED",
                "status": "SUCCESS",
                "url": "job/asgard/1/",
                "scm": {
                    "url": "https://github.com/Djiit/err-jenkins.git",
                    "branch": "origin/master",
                    "commit": "0e51ed"
                },
            }
        }
        result = jenkinsBot.JenkinsBot.format_notification(body)
        assert result == """Build #1 SUCCESS for Job dummy \
(http://jenkins.example.com/job/dummy/1/)
Based on https://github.com/Djiit/err-jenkins.git/commit/0e51ed \
(origin/master)"""
