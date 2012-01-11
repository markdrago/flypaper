#!/usr/bin/env python

import argparse
import json
import sys

from datetime import datetime, timedelta

from bug_list import BugList
from buggyfile_list import BuggyFileList
from changeset_list import ChangesetList
from repo_factory import RepoFactory


class FlyPaper(object):
    def __init__(self, bugid_file, repodir, startdate, showbugs,
                 output_format):
        self._bugid_file = bugid_file
        self._startdate = startdate
        self._showbugs = showbugs
        self._repodir = repodir
        self._output_format = output_format
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
        print self._get_output(results)

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
        #create dict mapping scores to buggy files
        score_map = {}
        for buggyfile in self._buggy_file_list.get_files():
            score = buggyfile.get_score(self._startdate)
            if score not in score_map:
                score_map[score] = []
            score_map[score].append(buggyfile)

        #create list sorted by score
        sorted_buggy_files = []
        all_scores = score_map.keys()
        all_scores.sort()
        all_scores.reverse()
        for score in all_scores:
            buggyfiles = score_map[score]
            buggyfiles.sort(cmp=lambda x, y: cmp(x.filename, y.filename))
            sorted_buggy_files.extend(buggyfiles)
        return sorted_buggy_files

    def _get_output(self, buggyfiles):
        if self._output_format == 'json':
            return self._get_output_json(buggyfiles)
        return self._get_output_plain_text(buggyfiles)

    def _get_output_plain_text(self, buggyfiles):
        output = ""
        for buggyfile in buggyfiles:
            score_str = "%.03f" % buggyfile.get_score(self._startdate)
            output += score_str + " " + buggyfile.filename
            if self._showbugs:
                buglist = [x.__str__() for x in buggyfile.get_bugs()]
                output += " "
                output += ",".join(buglist)
            output += "\n"
        return output

    def _get_output_json(self, buggyfiles):
        out_obj = {}
        files = []
        for buggyfile in buggyfiles:
            onefile = {}
            onefile['filename'] = buggyfile.filename
            onefile['score'] = buggyfile.get_score(self._startdate)
            if self._showbugs:
                onefile['bugs'] = [x.__str__() for x in buggyfile.get_bugs()]
            files.append(onefile)
        out_obj['files'] = files
        return json.dumps(out_obj, sort_keys=True, indent=2)

if __name__ == '__main__':
    description = 'Flypaper shows you the files which tend to attract bugs'
    parser = argparse.ArgumentParser(description)
    parser.add_argument('--buglist', default=sys.stdin,
                        type=argparse.FileType('r'),
                        help='a file which contains bug identifiers')
    parser.add_argument('--repo', default=None, type=unicode,
                        help='directory which contains a code repository')
    parser.add_argument('--startdate', default=None, type=unicode,
                        help='date to start looking in the repository')
    parser.add_argument('--showbugs', default=False, action='store_true',
                        help='show bug IDs in output')
    parser.add_argument('--output-format', default='plain', type=unicode,
                        help='set to json to get json output')
    parser.add_argument('--startoffset', default=None, type=int,
                        help='seconds ago to start looking in the repo')
    args = parser.parse_args()

    #default to starting one year ago
    startdate = datetime.now() - timedelta(seconds=31536000)
    if args.startoffset is not None:
        startdate = datetime.now() - timedelta(seconds=args.startoffset)
    elif args.startdate is not None:
        startdate = datetime.strptime(args.startdate, '%Y-%m-%d')

    flypaper = FlyPaper(args.buglist, args.repo, startdate,
                        args.showbugs, args.output_format)
    flypaper.show_bug_catchers()
