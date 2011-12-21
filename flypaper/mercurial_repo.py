import os
import subprocess
from datetime import datetime

from flypaper.changeset_list import ChangesetList
from flypaper.changeset import Changeset

class MercurialRepo(object):
    def __init__(self, repodir, startdate):
        self._repodir = repodir
        self._startdate = startdate

    def get_full_changesetlist(self):
        "return ChangesetList of all changesets since startdate"
        changeset_list = ChangesetList()
        self.add_changesets_with_dates_and_descriptions(changeset_list)
        self.add_modified_files_to_changeset_list(changeset_list)
        return changeset_list

    def add_modified_files_to_changeset_list(self, changeset_list):
        startdatestr = self._startdate.strftime('%Y-%m-%d')
        #note: getting files split on space may be a problem
        cmd = 'hg log -d ">' + startdatestr + '" --template "{node}|{files}\n"'
        result = self.get_command_output(cmd)

        for line in result.split('\n'):
            if line.strip() == '':
                continue
            (commitid, filenames) = line.split('|', 1)
            for filename in filenames.split(' '):
                filename = filename.strip()
                if len(filename) > 0:
                    changeset_list.changesets[commitid].add_modified_file(filename)

    def add_changesets_with_dates_and_descriptions(self, changeset_list):
        startdatestr = self._startdate.strftime('%Y-%m-%d')
        cmd = 'hg log -d ">' + startdatestr + '" --template "{node}|{date|shortdate}|{desc|firstline}\n"'
        result = self.get_command_output(cmd)

        for line in result.split('\n'):
            if line.strip() == '':
                continue
            (commitid, datestr, desc) = line.split('|', 2)
            date = datetime.strptime(datestr, '%Y-%m-%d')
            changeset_list.add(Changeset(self, commitid, date, desc))

    def get_command_output(self, cmd):
        "run a shell command and get the output"
        oldpath = os.getcwd()
        os.chdir(self._repodir)

        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        result = proc.communicate()[0]

        os.chdir(oldpath)
        return result

