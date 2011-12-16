#!/usr/bin/env python

import subprocess
import argparse
import sys
import os

class FlyPaper(object):
    def __init__(self, bugid_file, repodir, startdate):
        self._bugid_file = bugid_file
        self._repodir = repodir
        self._startdate = startdate

    def show_bug_catchers(self):
        self._buglist = BugList(self._bugid_file)
        self._repo = RepoFactory.get_repo(self._repodir, self._startdate)
        changesetlist = self._repo.get_full_changesetlist()
        changesetlist.remove_changesets_without_matching_description(self._buglist.bugids)
        
        files = {}
        for changeset in changesetlist.changesets:
            for filename in changeset.get_modified_files():
                if filename not in files:
                    files[filename] = 1
                else:
                    files[filename] += 1
        
        for filename in files:
            print str(files[filename]) + "  " + filename

class ChangesetList(object):
    def __init__(self):
        self.changesets = []
    
    def add(self, changeset):
        self.changesets.append(changeset)

    def remove_changesets_without_matching_description(self, bugids):
        bug_changesets = []
        for changeset in self.changesets:
            found_bug = False
            for bugid in bugids:
                if changeset.description_contains(bugid):
                    found_bug = True
                    break
            if found_bug:
                bug_changesets.append(changeset)
        self.changesets = bug_changesets

class Changeset(object):
    def __init__(self, repo, commitid, description=''):
        self._repo = repo
        self.commitid = commitid
        self.description = description

    def description_contains(self, needle):
        return needle in self.description

    def get_modified_files(self):
        return self._repo.get_files_modified_in_changeset(self.commitid)

    def get_score_for_fix_on_date(self, date):
        return 1

class RepoFactory(object):
    @classmethod
    def get_repo(clazz, repodir, startdate):
        if os.path.isdir(repodir + "/.hg"):
            return MercurialRepo(repodir, startdate)
        else:
            raise Exception("No support repository found in: %s" % (repodir,))

class MercurialRepo(object):
    def __init__(self, repodir, startdate):
        self._repodir = repodir
        self._startdate = startdate

    def get_full_changesetlist(self):
        "return ChangesetList of all changesets since startdate"
        cmd = 'hg log -d ">' + self._startdate + '" --template "{node}|{desc|firstline}\n"'
        result = self.get_command_output(cmd)

        changeset_list = ChangesetList()
        for line in result.split('\n'):
            if line.strip() == '':
                continue
            (commitid, desc) = line.split('|', 1)
            changeset_list.add(Changeset(self, commitid, desc))
        return changeset_list

    def get_files_modified_in_changeset(self, commitid):
        "return list of filenames modified in changeset"
        #note: getting files split on space may be a problem
        cmd = "hg log -r %s --template \"{files}\"" % (commitid,)
        result = self.get_command_output(cmd)
        return result.split(' ')

    def get_command_output(self, cmd):
        "run a shell command and get the output"
        oldpath = os.getcwd()
        os.chdir(self._repodir)

        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        result = proc.communicate()[0]

        os.chdir(oldpath)
        return result

class BugList(object):
    def __init__(self, bugid_file):
        self.bugids = []
        self._bugid_file = bugid_file
        self.read_bug_list()

    def read_bug_list(self):
        for line in self._bugid_file:
            self.bugids.append(line.strip())

if __name__ == '__main__':
    description = 'Flypaper shows you the files which tend to attract bugs'
    parser = argparse.ArgumentParser(description)
    parser.add_argument('--buglist', default=sys.stdin,
                        type=argparse.FileType('r'),
                        help='a file which contains bug identifiers')
    parser.add_argument('--repo', default=None, type=unicode,
                        help='directory which contains a code repository')
    parser.add_argument('--startdate', default='2011-01-01', type=unicode,
                        help='date to start looking in the repository')
    args = parser.parse_args()

    flypaper = FlyPaper(args.buglist, args.repo, args.startdate)
    flypaper.show_bug_catchers()

