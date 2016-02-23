import jenkinsBot


class TestJenkinsBot(object):
    extra_plugin_dir = '.'


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
_
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
                    "commit": "0e51ed9019bd39bdb77589be4f2634fb97b46fbc"
                },
                "artifacts": {
                    "dummy.tar.gz": {
                        "archive": "http://jenkins.example.com/job/dummy/1/artifact/dummy.tar.gz",
                        "s3": "https://s3-eu-west-1.amazonaws.com/dummy/dummy.tar.gz"
                    }
                }
            }
        }
        result = jenkinsBot.JenkinsBot.format_notification(body)
        assert result == """
"""
