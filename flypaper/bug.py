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

