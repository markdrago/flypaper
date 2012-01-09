#!/usr/bin/env python

import argparse
import sys

from datetime import datetime

from bug_list import BugList
from buggyfile_list import BuggyFileList
from changeset_list import ChangesetList
from repo_factory import RepoFactory


class FlyPaper(object):
    def __init__(self, bugid_file, repodir, startdate, showbugs):
        self._bugid_file = bugid_file
        self._startdate = startdate
        self._showbugs = showbugs
        self._repodir = repodir
        self._buglist = BugList()
        self._buggy_file_list = BuggyFileList()
        self._changesets = ChangesetList()

    def show_bug_catchers(self):
        #populate list of bugs
        self._buglist.read_bug_list(self._bugid_file)

        #populate list of changesets
        self._repo = RepoFactory.get_repo(self._repodir)
        self._repo.get_full_changesetlist(self._startdate, self._changesets)

        #match bugs with the changesets that fix them
        self._match_bugs_with_changesets()

        #forget changesets which do not fix a bug
        self._changesets.remove_changesets_which_do_not_fix_a_bug()

        #populate list of files which were modified when fixing bugs
        self._build_buggy_file_list()

        #sort files by bugginess and output results
        results = self._get_buggy_files_sorted_by_bugginess()
        self._print_results(results)

    def _match_bugs_with_changesets(self):
        for changeset in self._changesets.get_changesets():
            for bugid in self._buglist.bugs.keys():
                if changeset.description_contains(bugid):
                    bug = self._buglist.bugs[bugid]
                    bug.add_fixing_changeset(changeset)
                    changeset.add_bug_fixed(bug)

    def _build_buggy_file_list(self):
        for changeset in self._changesets.get_changesets():
            for filename in changeset.modified_files:
                for bug in changeset.bugs_fixed:
                    self._buggy_file_list.add_buggy_file(bug, filename)

    def _get_buggy_files_sorted_by_bugginess(self):
        scores = {}
        for buggyfile in self._buggy_file_list.get_files():
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
                    buglist = [x.__str__() for x in buggyfile.get_bugs()]
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
