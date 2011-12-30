import os
import subprocess
from datetime import datetime

from changeset_list import ChangesetList
from changeset import Changeset


class MercurialRepo(object):
    def __init__(self, repodir, startdate):
        self._repodir = repodir
        self._startdate = startdate

    #NOTE: Since a commit may have 0 files changed (merge), we add a preceding
    # '#' to the lines which contain the description and modified files.
    #We do this to avoid having 3 consecutive newlines.  That would cause a
    #problem since we're using newlines (and double newlines) as a delimiter.
    #We use newlines because they will not be present in the description once
    #we force it to just show the first line and it won't show up in the list
    #of files either.  This way we can get all of the data we need with one
    #command and we will be able to break it up safely and reliably.
    def get_full_changesetlist(self):
        "return ChangesetList of all changesets since startdate"
        changeset_list = ChangesetList()

        datestr = self._startdate.strftime('%Y-%m-%d')
        hg_format = '{node}\n{date|shortdate}\n#{desc|firstline}\n#{files}\n\n'
        cmd = 'hg log -d ">' + datestr + '" --template "' + hg_format + '"'
        result = self.get_command_output(cmd)

        for nodeblock in result.split("\n\n"):
            if nodeblock.strip() == '':
                continue

            (commitid, datestr, desc, files) = [
                x.strip() for x in nodeblock.split("\n", 3)
            ]

            #remove those awkward prefixed # characters
            desc = desc[1:]
            files = files[1:]

            date = datetime.strptime(datestr, '%Y-%m-%d')

            #create the base changeset and add it to the list
            changeset = Changeset(commitid, date, desc)
            changeset_list.add(changeset)

            #add the modified files to the changeset
            if files.strip() == '':
                continue
            for filename in files.split(' '):
                changeset.add_modified_file(filename)
        return changeset_list

    def get_command_output(self, cmd):
        "run a shell command and get the output"
        oldpath = os.getcwd()
        os.chdir(self._repodir)

        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        result = proc.communicate()[0]

        os.chdir(oldpath)
        return result
