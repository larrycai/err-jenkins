#!/usr/bin/python
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from jinja2 import Template
from jenkins import Jenkins
from errbot import BotPlugin, botcmd, webhook
from errbot.utils import ValidationException
try:
    from config import JENKINS_URL, JENKINS_USERNAME, JENKINS_PASSWORD
except ImportError:
    # Default configuration
    JENKINS_URL = ''
    JENKINS_USERNAME = ''
    JENKINS_PASSWORD = ''
    JENKINS_RECEIVE_NOTIFICATION = True


class JenkinsBot(BotPlugin):
    """Basic Err integration with Jenkins CI"""

    min_err_version = '1.2.1'
    #max_err_version = '3.3.0'

    def get_configuration_template(self):
        return {'URL': JENKINS_URL,
                'USERNAME': JENKINS_USERNAME,
                'PASSWORD': JENKINS_PASSWORD}

    def check_configuration(self, configuration):
        for c in configuration:
            if len(configuration[c] == 0):
                raise ValidationException(c)

    def connect_to_jenkins(self):
        """Connect to a Jenkins instance using configuration."""
        self.jenkins = Jenkins(url=self.config['URL'],
                               username=self.config['USERNAME'],
                               password=self.config['PASSWORD'])

    @webhook(r'/jenkins/notification')
    def handle_notification(self, incoming_request):
        if not JENKINS_RECEIVE_NOTIFICATION:
            return "Notification handling is disabled \
                    (JENKINS_RECEIVE_NOTIFICATION = False)"

        self.log.debug(repr(incoming_request))
        for room in self.bot_config.CHATROOM_PRESENCE:
            self.send(
                room,
                self.format_notification(incoming_request),
                message_type='groupchat'
            )
        return "OK"

    @botcmd
    def jenkins_list(self, mess, args):
        """List all jobs, optionally filter them using a search term."""
        self.connect_to_jenkins()

        search_term = args.strip().lower()
        jobs = self.search_job(search_term)
        return self.format_jobs(jobs)

    @botcmd
    def jenkins_running(self, mess, args):
        """List all running jobs."""
        self.connect_to_jenkins()

        jobs = [job for job in self.jenkins.get_jobs()
                if 'anime' in job['color']]
        return self.format_running_jobs(jobs)

    @botcmd
    def jenkins_param(self, mess, args):
        """List Parameters for a given job."""
        self.connect_to_jenkins()

        if len(args) == 0:
            return 'What Job would you like the parameters for?'
        if len(args.split()) > 1:
            return 'Please enter only one Job Name'

        if self.jenkins.get_job_info(args)['actions'][0] == {}:
            job_param = self.jenkins.get_job_info(
                args)['actions'][1]['parameterDefinitions']
        else:
            job_param = self.jenkins.get_job_info(
                args)['actions'][0]['parameterDefinitions']

        return self.format_params(job_param)

    @botcmd(split_args_with=None)
    def jenkins_build(self, mess, args):
        """Build a Jenkins Job with the given parameters
        Example: !jenkins build test_project FOO:bar
        """
        self.connect_to_jenkins()

        if len(args) == 0:  # No Job name
            return 'What job would you like to build?'

        params = self.build_parameters(args[1:])

        self.jenkins.build_job(args[0], params)
        running_job = self.search_job(args[0])
        return 'Your job should begin shortly: {0}'.format(
            self.format_jobs(running_job))

    def search_job(self, search_term):
        return [job for job in self.jenkins.get_jobs()
                if search_term.lower() in job['name'].lower()]

    def format_running_jobs(self, jobs):
        if len(jobs) == 0:
            return 'No running jobs.'

        jobs_info = [self.jenkins.get_job_info(job['name']) for job in jobs]
        return '\n\n'.join(['%s (%s)\n%s' % (
            job['name'],
            job['lastBuild']['url'],
            job['healthReport'][0]['description'])
                            for job in jobs_info]).strip()

    @staticmethod
    def format_jobs(jobs):
        if len(jobs) == 0:
            return 'No jobs found.'

        max_length = max([len(job['name']) for job in jobs])
        return '\n'.join(
            ['%s (%s)' % (job['name'].ljust(max_length), job['url'])
             for job in jobs]).strip()

    @staticmethod
    def format_params(job):
        PARAM_TEMPLATE = Template("""{% for p in job %} Type: {{p.type}}
Description: {{p.description}}
Default Value: {{p.defaultParameterValue.value}}
Parameter Name: {{p.name}}

{% endfor %}""")
        return PARAM_TEMPLATE.render(job)

    @staticmethod
    def build_parameters(params):
        if len(params) == 0:
            return {'': ''}
        return {param.split(':')[0]: param.split(':')[1]
                for param in params}

    @staticmethod
    def format_notification(body):
        NOTIFICATION_TEMPLATE = Template("""Build #{{build.numbner}} \
{{build.status}} for Job {{name}} ({{build.full_url}})
Based on {{build.scm.url}}@{{build.scm.commit}} ({{build.scm.branch}})
""")

        message = NOTIFICATION_TEMPLATE.render(**body)
        return body
