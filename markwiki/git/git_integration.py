# Copyright (c) 2016, deadc0de6
'''Versioning of the wiki pages through git'''
from sh import git

from markwiki.renderer import render_markdown_txt


class GitIntegration(object):

    GIT_MSG = 'change on page %s'

    def __init__(self, wiki_path):
        self.path = wiki_path
        self.git = git.bake(_cwd=self.path)
        self.git.init()
        self._set_config()
        self._bootstrap()

    def _bootstrap(self):
        self._add_untracked()
        self._add_local_change()

    def update_file(self, path):
        '''Called on each update of a wiki page.'''
        self._commit_file(path)

    def _set_config(self):
        '''Set git configs.'''
        self.git.config('--local', 'core.autocrlf', 'input')
        self.git.config('--local', 'user.name', 'markwiki')
        self.git.config('--local', 'user.email', '')

    def _add_untracked(self):
        '''Add individual commits for each untracked file.'''
        for f in self.git('ls-files', '--others').split('\n'):
            if f:
                self._commit_file(f)

    def _add_local_change(self):
        '''Commit local changes if any.'''
        for f in self.git('ls-files', '--modified').split('\n'):
            if f:
                self._commit_file(f)

    def _commit_file(self, path):
        '''Commit some change on a wiki page.'''
        self.git.add(path)
        msg = self.GIT_MSG % (path)
        self.git.commit('--message', msg)

    def get_changes(self, path):
        '''Get list of commits for a specific page.'''
        changes = []
        commits = self.git('--no-pager', 'log', '--format=%H,%ai', path)
        for commit in list(commits)[1:]:
            commit = commit.strip('\'')
            change = {}
            change['commit'] = commit.split(',')[0]
            change['date'] = commit.split(',')[1]
            changes.append(change)
        return changes

    def view_history(self, path, commit):
        '''View the file as it was at a specific commit.'''
        content = self.git('--no-pager', 'show', '%s:%s' % (commit, path))
        return render_markdown_txt(content)

    def revert_file(self, path, commit):
        '''Revert a file to a specific commit.'''
        self.git.checkout(commit, path)
        self._commit_file(path)
