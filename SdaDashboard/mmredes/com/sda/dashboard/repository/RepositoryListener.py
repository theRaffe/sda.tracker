import ConfigParser
import os
import shlex
import subprocess
import logging
import re

from mmredes.com.sda.dashboard.PersistentController import PersistentController
from mmredes.com.sda.utils import ConfigLogger

__author__ = 'macbook'
# ConfigLogger.get_sda_logger()
logger = logging.getLogger(__name__)


class RepositoryListener:
    repoDir = ''
    config_file = ''
    type_tech = None
    CONST_IS_BEHIND = 'branch is behind'
    id_branch = None

    def __init__(self, config_file="./board.cfg"):

        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        self.config_file = config_file
        self.repoDir = config.get('Repository', 'repo.dir')
        self.type_tech = config.get('Repository', 'type.tech')
        self.id_branch = config.get('Repository', 'id.branch')

    def command(self, cmd):
        logger.info('executing: %s at dir: %s' % (cmd, self.repoDir))
        pipe = subprocess.Popen(cmd, shell=True, cwd=self.repoDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, error_output) = pipe.communicate()
        if error_output:
            logger.warning("returning error_output = %s" % error_output)
        return out, error_output

    def rm_empty(self, L):
        return [l for l in L if (l and l != "")]

    def get_status(self):
        os.chdir(self.repoDir)
        self.command('git remote update')
        status, error_output = self.command("git status -u no")
        return status

    def grep(self, pattern, str_obj):
        grepper = re.compile(pattern)
        arr_str = str_obj.split('\n')
        for line in arr_str:
            if grepper.search(line):
                return line
        return None

    def get_list_merge_commit(self, current_branch):
        cmd1 = 'git rev-list %s...origin/%s' % (current_branch, current_branch)

        pipe1 = subprocess.Popen(shlex.split(cmd1), shell=True, cwd=self.repoDir, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        (output, error_output) = pipe1.communicate()
        list_result = []
        if not error_output:
            arr_commit = output.split('\n')
            for str_commit in arr_commit:
                cmd_git_show = 'git show %s' % str_commit
                cmd_grep = '"C:/progra~1/Git/usr/bin/grep.exe" Merge:'
                p_git_show = subprocess.Popen(shlex.split(cmd_git_show), shell=True, cwd=self.repoDir,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
                p_grep = subprocess.Popen(shlex.split(cmd_grep), shell=True, cwd=self.repoDir, stdin=p_git_show.stdout,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)

                (merge_commit, error_output) = p_grep.communicate()
                if merge_commit:
                    list_result.append(merge_commit)
                    logger.debug('merge_commit = %s' % merge_commit)
        else:
            logger.warning('error_output rev-list= %s' % error_output)

        return list_result

    def get_current_branch(self):
        output, error_output = self.command('git status')
        logger.info("output= %s" % output)
        status_line = [line for line in output.split('\n') if 'On branch' in line][0]
        arr_token = status_line.split(' ')
        return arr_token[2] if len(arr_token) == 3 else ''

    def is_behind(self):
        return self.CONST_IS_BEHIND in self.get_status()

    def get_branch_ticket(self, current_branch):
        logger.info("self.config_file= %s" % self.config_file)
        persistent_controller = PersistentController(self.config_file)
        dict_artifact = persistent_controller.get_artifacts()
        dict_branch = {}
        type_tech = self.type_tech

        # list_commit_merge = [line for line in commit_merge.split('\n') if line]
        list_commit_merge = self.get_list_merge_commit(current_branch)
        logger.debug("list_commit_merge=%s" % list_commit_merge)
        ls_commit_merge = []
        # for line in filter(None, commit_merge.split('\n')):
        for line in filter(None, list_commit_merge):
            # logger.info('line_commit_merge= %s' % line)
            ls_token_commit = line.split(' ')
            # the third token is the wanted commit
            # example: 'Merge: 93097c3 23e060e'
            ls_commit_merge.append(ls_token_commit[2])

        logger.debug('list of commits merge: %s' % ls_commit_merge)

        for commit_git in ls_commit_merge:
            # getting branch-ticket
            list_artifact = []

            cmd1 = 'git reflog --all'
            cmd2 = '"C:/progra~1/Git/usr/bin/grep.exe" %s' % commit_git
            pipe1 = subprocess.Popen(cmd1, shell=True, cwd=self.repoDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pipe2 = subprocess.Popen(cmd2, shell=True, cwd=self.repoDir, stdin=pipe1.stdout, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            (output, error_output) = pipe2.communicate()
            if error_output:
                logger.warning('git reflog error: %s' % error_output)
            # output, error_output = self.command('git reflog --all | grep %s' % commit_git)
            if not output:
                continue
            logger.info('output of git reflog: %s' % output)
            ref_log = [token_log for token_log in output.split(' ') if '@' in token_log][0]
            # iterating of tokens refs/remotes/origin/{branch}@{0}
            # getting token with a @ then get token branch
            ls_token_reflog = [token_reflog.split('@')[0] for token_reflog in ref_log.split('/') if '@' in token_reflog]
            branch = ls_token_reflog[0]

            str_command = 'git show --pretty="format:%%ae" --name-only %s' % commit_git
            modified_files, error_output = self.command(str_command)
            # print modified_files

            list_modified_files = filter(None, modified_files.split('\n'))
            email = list_modified_files[0]
            list_files = list_modified_files[1:]
            # for modified_file in list_modified_files[1:]:
            #    list_files.append(modified_file)
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
                list_found_artifact = [item for item in ls_branch_artifact if item['id_artifact'] == id_artifact and item['email'] == email and item['id_type_tech'] == type_tech]
                if len(list_found_artifact) == 0:
                    dict_result = {'id_artifact': id_artifact, 'email': email, 'id_type_tech': type_tech}
                    ls_branch_artifact.append(dict_result)
            dict_branch[branch] = ls_branch_artifact

        return dict_branch, self.id_branch

    def update_local_repository(self):
        return self.command('git pull')
