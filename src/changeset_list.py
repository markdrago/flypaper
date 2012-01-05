class ChangesetList(object):
    def __init__(self):
        self._changesets = {}

    def add(self, changeset):
        self._changesets[changeset.commitid] = changeset

    def get_changesets(self):
        return self._changesets.values()

    def remove_changesets_which_do_not_fix_a_bug(self):
        changesets_fixing_bugs = {}
        for commit_id in self._changesets:
            if self._changesets[commit_id].bugs_fixed_count() > 0:
                changesets_fixing_bugs[commit_id] = self._changesets[commit_id]
        self._changesets = changesets_fixing_bugs
