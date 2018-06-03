import os
import re
import logging
from collections import Counter
from functools import partial

import asana


logging.basicConfig(level=logging.INFO)

TAKE_COURSE_PAT = r'^\d+\)'
AUDIT_PAT = r'^\d+\]'

personal_access_token = os.environ.get('ASANA_TOKEN')
client = asana.Client.access_token(personal_access_token)
client.options['project'] = os.environ.get('PROJECT_ID')


def task_name_filter(task, re_pattern):
    return re.search(re_pattern, task['name'])


take_course_filter = partial(task_name_filter, re_pattern=TAKE_COURSE_PAT)
audit_filter = partial(task_name_filter, re_pattern=AUDIT_PAT)


def reviewer_filter(task):
    return (
        '/' in task['name'] and
        '審核者' not in task['name']
    )


def check_reviewer_in_subtasks(task, reviewer_name):
    subtasks = client.tasks.subtasks(task['id'])
    reviewer_subtasks = filter(reviewer_filter, subtasks)
    for subtask in reviewer_subtasks:
        if reviewer_name in subtask['name']:
            return True
    return False


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('reviewer_name',
                        help='Name of target reviewer')
    parser.add_argument('-a', '--audit',
                        help='Check audit tasks',
                        action='store_false')
    parser.add_argument('-t', '--take-course',
                        help='Check take course tasks',
                        action='store_false')
    args = parser.parse_args()

    tasks = list(client.tasks.find_all())

    target_tasks = list()
    if args.take_course:
        target_tasks += list(filter(take_course_filter, tasks))

    if args.audit:
        target_tasks += list(filter(audit_filter, tasks))

    for task in target_tasks:
        try:
            if not check_reviewer_in_subtasks(task, args.reviewer_name):
                print(task['name'])
        except Exception as err:
            logging.error(
                (
                    f"Error occurs on {task['name']}\n"
                    f"Exception: {err}"
                )
            )
