#!/usr/bin/env python

import argparse
import sys

from datetime import datetime

from bug_list import BugList
from buggyfile_list import BuggyFileList
from repo_factory import RepoFactory


class FlyPaper(object):
    def __init__(self, bugid_file, repodir, startdate, showbugs):
        self._bugid_file = bugid_file
        self._repodir = repodir
        self._startdate = startdate
        self._showbugs = showbugs

    def show_bug_catchers(self):
        self._buglist = BugList()
        self._buglist.read_bug_list(self._bugid_file)
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
                    buglist = [x.__str__() for x in buggyfile.bugs.values()]
                    output += " "
                    output += ",".join(buglist)
                print output

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
