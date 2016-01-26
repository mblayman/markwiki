import git
import os

class GitIntegration(object):

    GIT_MSG = 'change on page \"%s\"'

    def __init__(self, wiki_path, remote=None):
        self.repo = git.Repo.init(wiki_path)
        if remote:
            origin = self.repo.create_remote('origin', remote)
            origin.fetch()
            origin.pull(origin.refs[0].remote_head)

    def _add_all(self):
        self.repo.git.add('--all')
        self.repo.index.commit('adding uncommitted changes')

    def bootstrap(self):
        if len(self.repo.untracked_files) > 0:
            self._add_all()

    def update_file(self, path, content):
        with open(path, 'wb') as f:
            f.write(content)
        self.repo.index.add([path])
        self.repo.index.commit(self.GIT_MSG % (os.path.basename(path)))

    def get_change(self, path):
        # TODO should return last change for path
        pass

    def revert_file(self, path):
        # TODO should revert file to last commit
        pass
        #self.repo.index.checkout([path], force=False)

    # check if origin has changed
    def _change_with_origin(self):
        local = self.repo.commit()
        remote = self.repo.origin.fetch()[0].commit
        return local.hexsha == remote.hexsha
