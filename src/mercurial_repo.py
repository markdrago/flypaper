import os
import subprocess
from datetime import datetime

from changeset_list import ChangesetList
from changeset import Changeset


class MercurialRepo(object):
    def __init__(self, repodir):
        self._repodir = repodir

    #NOTE: Since a commit may have 0 files changed (merge), we add a preceding
    # '#' to the lines which contain the description and modified files.
    #We do this to avoid having 3 consecutive newlines.  That would cause a
    #problem since we're using newlines (and double newlines) as a delimiter.
    #We use newlines because they will not be present in the description once
    #we force it to just show the first line and it won't show up in the list
    #of files either.  This way we can get all of the data we need with one
    #command and we will be able to break it up safely and reliably.
    def get_full_changesetlist(self, startdate):
        "return ChangesetList of all changesets since startdate"
        datestr = startdate.strftime('%Y-%m-%d')
        hg_format = '{node}\n{date|shortdate}\n#{desc|firstline}\n#{files}\n\n'
        cmd = 'hg log -d ">' + datestr + '" --template "' + hg_format + '"'
        result = self.get_command_output(cmd)
        return self._create_changeset_list(result)

    def _create_changeset_list(self, full_logoutput):
        changeset_list = ChangesetList()
        for nodeblock in full_logoutput.split("\n\n"):
            changeset = self._create_single_changeset(nodeblock)
            if changeset is not None:
                changeset_list.add(changeset)
        return changeset_list

    def _create_single_changeset(self, logoutput):
        if logoutput.strip() == '':
            return None

        (commitid, datestr, desc, files) = [
            x.strip() for x in logoutput.split("\n", 3)
        ]

        #remove those awkward prefixed # characters
        desc = desc[1:].strip()
        files = files[1:].strip()

        date = datetime.strptime(datestr, '%Y-%m-%d')

        #create the base changeset
        changeset = Changeset(commitid, date, desc)

        #add the modified files to the changeset
        if files.strip() != '':
            for filename in files.split(' '):
                changeset.add_modified_file(filename)
        return changeset

    def get_command_output(self, cmd):
        "run a shell command and get the output"
        oldpath = os.getcwd()
        os.chdir(self._repodir)

        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        result = proc.communicate()[0]

        os.chdir(oldpath)
        return result
