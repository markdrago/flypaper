class BuggyFile(object):
    def __init__(self, filename):
        self.score = None
        self.filename = filename
        self._bugs = {}

    def add_bug(self, bug):
        if bug.bugid not in self._bugs:
            self._bugs[bug.bugid] = bug

    def get_score(self, startdate):
        '''the score for a file is the sum of the score for the bugs
           which were in it'''
        if self.score is None:
            self.score = sum([bug.get_score(startdate) for bug in self._bugs.values()])
        return self.score

