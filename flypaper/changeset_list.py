class ChangesetList(object):
    def __init__(self):
        self.changesets = {}

    def add(self, changeset):
        self.changesets[changeset.commitid] = changeset

    def remove_changesets_which_do_not_fix_a_bug(self):
        changesets_fixing_bugs = {}
        for commit_id in self.changesets:
            if self.changesets[commit_id].bugs_fixed_count() > 0:
                changesets_fixing_bugs[commit_id] = self.changesets[commit_id]
        self.changesets = changesets_fixing_bugs
