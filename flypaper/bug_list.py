from bug import Bug

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

