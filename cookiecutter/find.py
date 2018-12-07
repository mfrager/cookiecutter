# -*- coding: utf-8 -*-

"""Functions for finding Cookiecutter templates and other components."""

import logging
import os

from .exceptions import NonTemplatedInputDirException

logger = logging.getLogger(__name__)


def find_template(repo_dir, context):
    """Determine which child directory of `repo_dir` is the project template.

    :param repo_dir: Local directory of newly cloned repo.
    :returns project_template: Relative path to project template.
    """
    logger.debug('Searching {} for the project template.'.format(repo_dir))

    repo_dir_contents = os.listdir(repo_dir)

    project_template = None

    delim_start = '{{'
    delim_end = '}}'
    environment = context.get('_environment')
    if environment:
        if 'variable_start_string' in environment:
            delim_start = environment['variable_start_string']
        if 'variable_end_string' in environment:
            delim_end = environment['variable_end_string']

    for item in repo_dir_contents:
        if 'cookiecutter' in item and delim_start in item and delim_end in item:
            project_template = item
            break

    if project_template:
        project_template = os.path.join(repo_dir, project_template)
        logger.debug(
            'The project template appears to be {}'.format(project_template)
        )
        return project_template
    else:
        raise NonTemplatedInputDirException
