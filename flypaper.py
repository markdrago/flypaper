#!/usr/bin/env python

import subprocess
import argparse
import math
import sys
import os

from datetime import datetime

class FlyPaper(object):
    def __init__(self, bugid_file, repodir, startdate, showbugs):
        self._bugid_file = bugid_file
        self._repodir = repodir
        self._startdate = startdate
        self._showbugs = showbugs

    def show_bug_catchers(self):
        self._buglist = BugList(self._bugid_file)
        self._repo = RepoFactory.get_repo(self._repodir, self._startdate)
        self._changesetlist = self._repo.get_full_changesetlist()

        self._match_bugs_with_changesets()
        self._changesetlist.remove_changesets_which_do_not_fix_a_bug()

        self._build_buggy_file_list()
        results = self._get_buggy_files_sorted_by_bugginess()
        self._print_results(results)

    def _build_buggy_file_list(self):
        self._buggy_file_list = BuggyFileList()
        for changeset in self._changesetlist.changesets.values():
            for filename in changeset.modified_files:
                for bug in changeset.bugs_fixed:
                    self._buggy_file_list.add_buggy_file(bug, filename)

    def _match_bugs_with_changesets(self):
        for changeset in self._changesetlist.changesets.values():
            for bugid in self._buglist.bugs.keys():
                if changeset.description_contains(bugid):
                    bug = self._buglist.bugs[bugid]
                    bug.add_fixing_changeset(changeset)
                    changeset.add_bug_fixed(bug)

    def _get_buggy_files_sorted_by_bugginess(self):
        scores = {}
        for buggyfile in self._buggy_file_list.filenames.values():
            score = buggyfile.get_score(self._startdate)
            if score not in scores:
                scores[score] = []
            scores[score].append(buggyfile)
        return scores

    def _print_results(self, results):
        scores = results.keys()
        scores.sort()
        for score in scores:
            buggyfiles = results[score]
            buggyfiles.sort(cmp=lambda x, y: cmp(x.filename, y.filename))
            for buggyfile in buggyfiles:
                output = "%.03f" % score + " " + buggyfile.filename
                if self._showbugs:
                    output += " "
                    output += ",".join([x.__str__() for x in buggyfile.bugs.values()])
                print output

class Bug(object):
    def __init__(self, bugid):
        self.score = None
        self.bugid = bugid
        self.fixing_changesets = set()

    def add_fixing_changeset(self, changeset):
        self.fixing_changesets.add(changeset)

    def get_score(self, startdate):
        if self.score is None:
            self.score = max([chg.get_score(startdate) for chg in self.fixing_changesets])
        return self.score
    
    def __str__(self):
        return str(self.bugid)

class BugList(object):
    def __init__(self, bugid_file):
        self._bugid_file = bugid_file
        self.read_bug_list()

    def read_bug_list(self):
        self.bugs = {}
        for line in self._bugid_file:
            bugid = line.strip()
            bug = Bug(bugid)
            self.bugs[bugid] = bug

class BuggyFile(object):
    def __init__(self, filename):
        self.score = None
        self.filename = filename
        self.bugs = {}

    def add_bug(self, bug):
        if bug.bugid not in self.bugs:
            self.bugs[bug.bugid] = bug

    def get_score(self, startdate):
        if self.score is None:
            self.score = sum([bug.get_score(startdate) for bug in self.bugs.values()])
        return self.score

class BuggyFileList(object):
    def __init__(self):
        self.filenames = {}

    def add_buggy_file(self, bug, filename):
        if filename not in self.filenames:
            self.filenames[filename] = BuggyFile(filename)
        self.filenames[filename].add_bug(bug)

class Changeset(object):
    def __init__(self, repo, commitid, date, description=''):
        self.score = None
        self._repo = repo
        self.commitid = commitid
        self.description = description
        self.date = date
        self.bugs_fixed = set()
        self.modified_files = set()

    def description_contains(self, needle):
        return needle in self.description

    def add_bug_fixed(self, bug):
        self.bugs_fixed.add(bug)

    def add_modified_file(self, filename):
        self.modified_files.add(filename)

    def get_score(self, startdate):
        if self.score is None:
            self.score = self._calculate_score(startdate)
        return self.score

    def _calculate_score(self, startdate):
        today = datetime.today().replace(hour=0, minute=0, second=0)
        total_diff = today - startdate
        changeset_diff = self.date - startdate

        time_ratio = changeset_diff.total_seconds() / total_diff.total_seconds()

        return 1 / (1 + math.exp((-3 * time_ratio) + 3))

class ChangesetList(object):
    def __init__(self):
        self.changesets = {}

    def add(self, changeset):
        self.changesets[changeset.commitid] = changeset

    def remove_changesets_which_do_not_fix_a_bug(self):
        changesets_with_bugs_fixed = {}
        for commit_id in self.changesets:
            if len(self.changesets[commit_id].bugs_fixed) > 0:
                changesets_with_bugs_fixed[commit_id] = self.changesets[commit_id]
        self.changesets = changesets_with_bugs_fixed

class RepoFactory(object):
    @classmethod
    def get_repo(clazz, repodir, startdate):
        if os.path.isdir(repodir + "/.hg"):
            return MercurialRepo(repodir, startdate)
        else:
            raise Exception("No supported repository found in: %s" % (repodir,))

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
    parser.add_argument('--showbugs', default=False, action='store_true',
                        help='show bug IDs in output')
    args = parser.parse_args()

    flypaper = FlyPaper(args.buglist,
                        args.repo,
                        datetime.strptime(args.startdate, '%Y-%m-%d'),
                        args.showbugs)
    flypaper.show_bug_catchers()

