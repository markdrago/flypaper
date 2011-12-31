import math
from datetime import datetime


class Changeset(object):
    def __init__(self, commitid, date, description=''):
        self.score = None
        self.commitid = commitid
        self.description = description
        self.date = date
        self.bugs_fixed = set()
        self.modified_files = set()

    def description_contains(self, needle):
        return needle in self.description

    def bugs_fixed_count(self):
        return len(self.bugs_fixed)

    def add_bug_fixed(self, bug):
        self.bugs_fixed.add(bug)

    def add_modified_file(self, filename):
        self.modified_files.add(filename)

    def get_score(self, startdate):
        if self.score is None:
            self.score = self._calculate_score(startdate, datetime.today())
        return self.score

    def _get_date_ratio(self, startdate, today):
        today = today.replace(hour=0, minute=0, second=0)
        startdate = startdate.replace(hour=0, minute=0, second=0)
        total_diff = today - startdate
        changeset_diff = self.date - startdate

        return changeset_diff.total_seconds() / total_diff.total_seconds()

    def _calculate_score(self, date_ratio, scale=3):
        return 1 / (1 + math.exp(((-1 * scale) * date_ratio) + scale))
