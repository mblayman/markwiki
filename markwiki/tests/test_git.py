# Copyright (c) 2016, deadc0de6
'''Basic tests for git integration.'''

import unittest
import os
import tempfile
import random
import string
import shutil

from markwiki.git.git_integration import GitIntegration


class TestGitIntegration(unittest.TestCase):

    STRINGLEN = 10
    MASTERPATH = '.git/logs/refs/heads/master'
    TMPSUFFIX = 'markwikigit'

    def get_string(self):
        '''get a random string of length STRINGLEN'''
        alpha = string.ascii_uppercase + string.digits
        return ''.join(random.choice(alpha) for _ in range(self.STRINGLEN))

    def get_tmpdir(self):
        '''return a temporary directory for tests'''
        return tempfile.mkdtemp(suffix=self.TMPSUFFIX)

    def create_file(self, folder):
        '''create a new file in folder with random content'''
        self.assertTrue(os.path.exists(folder))
        fname = self.get_string()
        content = self.get_string()
        open(os.path.join(folder, fname), 'w').write(content)
        return fname, content

    def change_content(self, folder, path):
        '''change content of file'''
        self.assertTrue(os.path.exists(folder))
        fpath = os.path.join(folder, path)
        self.assertTrue(os.path.exists(fpath))
        content = self.get_string()
        open(fpath, 'w').write(content)
        return content

    def get_content(self, folder, path):
        '''return content of file'''
        self.assertTrue(os.path.exists(folder))
        fpath = os.path.join(folder, path)
        self.assertTrue(os.path.exists(fpath))
        return open(fpath, 'r').read()

    def clean(self, path):
        '''rm -r folder'''
        shutil.rmtree(path)

    def test_gitinit(self):
        '''test git init is done properly by checking git config file'''
        gitpath = self.get_tmpdir()
        git = GitIntegration(gitpath)

        subpath = os.path.join(gitpath, '.git')
        self.assertTrue(os.path.exists(subpath))
        cfgpath = os.path.join(subpath, 'config')
        self.assertTrue(os.path.exists(cfgpath))

        # check we have markwiki in config (user.name)
        cfg = open(cfgpath, 'r').read()
        self.assertTrue('markwiki' in cfg)
        self.clean(gitpath)

    def test_gitadduntracked(self):
        '''test git adds untracked files'''
        gitpath = self.get_tmpdir()
        newfile, _ = self.create_file(gitpath)

        # check new file is in git
        git = GitIntegration(gitpath)
        head = self.get_content(gitpath, self.MASTERPATH)
        self.assertTrue(newfile in head)
        self.clean(gitpath)

    def test_gitcommit(self):
        '''test git commits new file'''
        gitpath = self.get_tmpdir()
        git = GitIntegration(gitpath)

        # create a new file
        newfile, _ = self.create_file(gitpath)
        git.update_file(newfile)

        # make sure the file is referenced in HEAD
        head = self.get_content(gitpath, self.MASTERPATH)
        self.assertTrue(newfile in head)
        self.clean(gitpath)

    def test_githistory(self):
        '''make sure we're able to retrieve old version of files'''
        gitpath = self.get_tmpdir()
        git = GitIntegration(gitpath)

        # create a new file
        newfile, _ = self.create_file(gitpath)
        git.update_file(newfile)

        # change file's content
        newcontent = self.change_content(gitpath, newfile)
        git.update_file(newfile)

        # check file history is not empty
        self.assertTrue(git.get_changes(newfile) != [])
        self.clean(gitpath)

    def test_gitrevert(self):
        '''make sure we can revert file'''
        gitpath = self.get_tmpdir()
        git = GitIntegration(gitpath)

        # create a new file
        newfile, oldcontent = self.create_file(gitpath)
        git.update_file(newfile)

        # change file content
        newcontent = self.change_content(gitpath, newfile)
        git.update_file(newfile)

        # check changes is not empty
        commits = git.get_changes(newfile)
        self.assertEqual(type(commits), list)
        self.assertTrue(len(commits) > 0)

        # revert the file and get content
        commit = commits[0]['commit']
        git.revert_file(newfile, commit)
        revcontent = self.get_content(gitpath, newfile)

        # check reverted file's content is the same as initial content
        self.assertEqual(revcontent, oldcontent)
        self.clean(gitpath)
