#!/usr/bin/env python

import subprocess
import argparse
import sys
import os

class FlyPaper(object):
    def __init__(self, bugid_file, repodir, startdate):
        self.bugid_file = bugid_file
        self.repodir = repodir
        self.startdate = startdate

    def show_bug_catchers(self):
        self.buglist = BugList(self.bugid_file)
        self.repo = Repo(self.repodir, self.startdate)
        changesetlist = self.repo.get_full_changesetlist()
        changesetlist.remove_changesets_without_matching_description(self.buglist.get_bugids())
        
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
    
    def add(self,  changeset):
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
    def __init__(self, repo, hexid, description=''):
        self.repo = repo
        self.hexid = hexid
        self.set_description(description)

    def get_hexid(self):
        return self.hexid

    def set_description(self, description):
        self.description = description
    
    def get_description(self):
        return self.description

    def description_contains(self, needle):
        return needle in self.description

    def get_modified_files(self):
        return self.repo.get_files_modified_in_changeset(self.hexid)

    def get_score_for_fix_on_date(self, date):
        return 1

class Repo(object):
    def __init__(self, repodir, startdate):
        self.repodir = repodir
        self.startdate = startdate
        self.get_full_changesetlist()

    def get_full_changesetlist(self):
        "return ChangesetList of all changesets since startdate"
        cmd = 'hg log -d ">' + self.startdate + '" --template "{node}|{desc|firstline}\n"'
        result = self.get_command_output(cmd)

        changeset_list = ChangesetList()
        for line in result.split('\n'):
            if line.strip() == '':
                continue
            (hexid, desc) = line.split('|', 1)
            changeset_list.add(Changeset(self, hexid, desc))
        return changeset_list

    def get_files_modified_in_changeset(self, hexid):
        "return list of filenames modified in changeset"
        #note: getting files split on space may be a problem
        cmd = "hg log -r %s --template \"{files}\"" % (hexid,)
        result = self.get_command_output(cmd)
        return result.split(' ')

    def get_command_output(self, cmd):
        "run a shell command and get the output"
        oldpath = os.getcwd()
        os.chdir(self.repodir)

        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        result = proc.communicate()[0]

        os.chdir(oldpath)
        return result

class BugList(object):
    def __init__(self, bugid_file):
        self.bugids = []
        self.bugid_file = bugid_file
        self.read_bug_list()

    def read_bug_list(self):
        for line in self.bugid_file:
            self.bugids.append(line.strip())

    def get_bugids(self):
        return self.bugids

if __name__ == '__main__':
    description = 'Flypaper shows you the files which attract bugs'
    parser = argparse.ArgumentParser(description)
    parser.add_argument('--buglist', default=sys.stdin,
                        type=argparse.FileType('r'),
                        help='a file which contains bug identifiers')
    parser.add_argument('--hgrepo', default=None, type=unicode,
                        help='directory which contains a mercurial repo')
    parser.add_argument('--startdate', default='2011-01-01', type=unicode,
                        help='date to start looking in the repository')
    args = parser.parse_args()

    flypaper = FlyPaper(args.buglist, args.hgrepo, args.startdate)
    flypaper.show_bug_catchers()

