# -*- coding: utf-8 -*-
# !/Volumes/Develop/develop/virtual_env_list/redmine_alfred/venv/bin/python3

import sys
import os
import alp

# path = os.path.dirname(os.path.abspath(__file__))
path = "/Volumes/Develop/develop/virtual_env_list/redmine_alfred/"
# print(path)
activate_this = os.path.join(path, 'venv', 'bin', 'activate_this.py')
activate_this_file = activate_this
# print(activate_this_file)
exec(compile(open(activate_this_file, "rb").read(), activate_this_file, 'exec'), dict(__file__=activate_this_file))


import subprocess
from redminelib import Redmine


REDMINE_URL = 'https://redmine.piolink.com'
REDMINE_KEY = '10220f473b65e8ebbfa79ddfaa506592ece5d82a'
ISSUE_FMT = "#{} {}"


def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))


class QuickRedmine(object):
    def __init__(self):
        self.redmine = Redmine(
            REDMINE_URL, key=REDMINE_KEY, request={'verify': False})

    def get_subject(self, issue_num):
        issue = self.redmine.issue.get(issue_num)
        return issue.subject


if __name__== "__main__":
    qr = QuickRedmine()
    issue_num = int(sys.argv[1])

    # Crawling Redmine subject
    subject = qr.get_subject(issue_num)
    subject = ISSUE_FMT.format(issue_num, subject)
    write_to_clipboard(subject)

    # Add Redmine Subject to Alfred Object

    subjectDic = dict(title=str(subject), subtitle="Redmine", uid="subject", valid=True, arg=str(issue_num), icon="/Users/leejunghwa/Documents/configuration/redmine_alfred/redmine.png")
    subject_item = alp.Item(**subjectDic)

    itemsList = [subject_item]
    alp.feedback(itemsList)
