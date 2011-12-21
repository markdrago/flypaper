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

