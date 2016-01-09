import ConfigParser
import os
import subprocess
import logging

from mmredes.com.sda.dashboard.PersistentController import PersistentController

__author__ = 'macbook'
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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

    def get_current_branch(self):
        output = self.command('git status')
        status_line = [line for line in output.split('\n') if 'On branch' in line][0]
        arr_token = status_line.split(' ')
        return arr_token[2] if len(arr_token) == 3 else ''


    def is_behind(self):
        return self.CONST_IS_BEHIND in self.get_status()

    def get_branch_ticket(self, current_branch):
        print ("self.config_file", self.config_file)
        persistentController = PersistentController(self.config_file)
        dict_artifact = persistentController.get_artifacts()
        dict_branch = {}
        type_tech = self.type_tech

        str_command = 'git rev-list %s...origin/%s | xargs git show | grep Merge:' % (current_branch, current_branch)
        commit_merge = self.command(str_command)
        ls_commit_merge = []
        for line in filter(None, commit_merge.split('\n')):
            # logger.info(line)
            ls_token_commit = line.split(' ')
            # the third token is the wanted commit
            # example: 'Merge: 93097c3 23e060e'
            ls_commit_merge.append(ls_token_commit[2])

        logger.info('list of commits merge: %s' % ls_commit_merge)

        for commit_git in ls_commit_merge:
            # getting branch-ticket
            list_artifact = []
            output = self.command('git reflog --all | grep %s' % commit_git)
            if output == '':
                continue
            logger.info('output of git reflog: %s' % output)
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
            logger.info('branch:{0:s} email: {1:s}'.format(branch, email))
            logger.info('files: %s' % list_files)
            # Iterate each path
            # and determine artifact by getting the first directory of each path file
            for file_path in list_files:
                list_token = file_path.split('/')
                if len(list_token) > 1:
                    path_directory = list_token[0]
                    id_artifact = dict_artifact[path_directory] if dict_artifact[path_directory] else -1
                    if id_artifact not in list_artifact:
                        list_artifact.append(id_artifact)
            logger.info('branch [%s] list of artifact: %s' % (branch, list_artifact))
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
