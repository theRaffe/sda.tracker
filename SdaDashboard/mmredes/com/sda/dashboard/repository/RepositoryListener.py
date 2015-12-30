import ConfigParser
import os
import subprocess

from mmredes.com.sda.dashboard.PersistentController import PersistentController

__author__ = 'macbook'

class RepositoryListener:
    repoDir = ''
    config_file = ''
    type_tech = None
    CONST_IS_BEHIND = 'branch is behind'
    id_branch = None

    def __init__(self, config_file = "./board.cfg"):

        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        self.config_file = config_file
        self.repoDir = config.get('Repository', 'repo.dir')
        self.type_tech = config.get('Repository', 'type.tech')
        self.id_branch = config.get('Repository', 'id.branch')

    def command(self, cmd):
        pipe = subprocess.Popen(cmd, shell=True, cwd=self.repoDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, error) = pipe.communicate()
        return out

    def rm_empty(self, L):
        return [l for l in L if (l and l != "")]

    def get_status(self):
        os.chdir(self.repoDir)
        self.command('git remote update')
        status = self.command("git status -u no")
        return status

    def is_behind(self):
        return self.CONST_IS_BEHIND in self.get_status()

    def get_branch_ticket(self):
        print ("self.config_file", self.config_file)
        persistentController = PersistentController(self.config_file)
        dict_artifact = persistentController.get_artifacts()
        dict_branch = {}
        type_tech = self.type_tech

        commit_merge = self.command('git rev-list develop...origin/develop | xargs git show | grep commit ')
        ls_commit_merge = []
        for line in filter(None, commit_merge.split('\n')):
            print(line)
            ls_token_commit = line.split(' ')
            # the third token is the wanted commit
            # example: 'Merge: 93097c3 23e060e'
            ls_commit_merge.append(ls_token_commit[2])

        print(ls_commit_merge)

        for commit_git in ls_commit_merge:
            # getting branch-ticket
            list_artifact = []
            output = self.command('git reflog --all | grep %s' % commit_git)
            print output
            ref_log = [token_log for token_log in output.split(' ') if '@' in token_log][0]
            # iterating of tokens refs/remotes/origin/{branch}@{0}
            # getting token with a @ then get token branch
            ls_token_reflog = [token_reflog.split('@')[0] for token_reflog in ref_log.split('/') if '@' in token_reflog]
            branch = ls_token_reflog[0]

            str_command = 'git show --pretty="format:%%ae" --name-only %s' % commit_git
            modified_files = self.command(str_command)
            # print modified_files
            email = ''
            list_files = []
            for file in filter(None, modified_files.split('\n')):
                if '@' in file:
                    email = file
                else:
                    list_files.append(file)
            print 'branch:{0:s} email: {1:s}'.format(branch, email)
            print ('files', list_files)
            # Iterate each path
            # and determinate artifact by getting the first directory of each path file
            for file_path in list_files:
                list_token = file_path.split('/')
                if len(list_token) > 1:
                    path_directory = list_token[0]
                    id_artifact = dict_artifact[path_directory] if dict_artifact[path_directory] else -1
                    if id_artifact not in list_artifact:
                        list_artifact.append(id_artifact)
            print(list_artifact)
            if branch in dict_branch:
                ls_branch_artifact = dict_branch[branch]
            else:
                ls_branch_artifact = []
            for id_artifact in list_artifact:
                dict = {'id_artifact': id_artifact, 'email': email, 'id_type_tech': type_tech}
                ls_branch_artifact.append(dict)
            dict_branch[branch] = ls_branch_artifact

        return dict_branch, self.id_branch

    def update_local_repository(self):
        return self.command('git pull')
