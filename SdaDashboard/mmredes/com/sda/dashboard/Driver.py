import time, sys
import os
import string
from mmredes.com.sda.dashboard.DriverDao import DriverDao
# from subprocess import subprocess
import subprocess

repoDir = '/Users/macbook/Documents/workspaces/git/rafe.first.rep'
CONST_IS_BEHIND = 'branch is behind'


def command(cmd):
    # return str(Popen(x.split(' '), stdout=PIPE).communicate()[0])
    pipe = subprocess.Popen(cmd, shell=True, cwd=repoDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, error) = pipe.communicate()
    return out


def rm_empty(L): return [l for l in L if (l and l != "")]


def get_status():
    os.chdir(repoDir)
    command('git remote update')
    status = command("git status -u no")
    return status


def is_behind():
    return CONST_IS_BEHIND in get_status()


__author__ = 'macbook'
if __name__ == '__main__':
    # x = 1
    # while True:
    #     try:
    #         print x
    #         time.sleep(1)
    #         x += 1
    #     except KeyboardInterrupt:
    #         print "Quit! See you"
    #         sys.exit()
    is_branch_behind = is_behind()
    print("is behind ", is_branch_behind)
    if is_branch_behind:
        driverDao = DriverDao()
        dict_artifact = driverDao.get_artifacts()
        dict_branch = {}
        type_tech = 1

        commit_merge = command('git rev-list HEAD...origin/develop | xargs git show | grep Merge:')
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
            output = command('git reflog --all | grep %s' % commit_git)
            print output
            ref_log = [token_log for token_log in output.split(' ') if '@' in token_log][0]
            # iterating of tokens refs/remotes/origin/{branch}@{0}
            # getting token with a @ then get token branch
            ls_token_reflog = [token_reflog.split('@')[0] for token_reflog in ref_log.split('/') if '@' in token_reflog]
            branch = ls_token_reflog[0]

            str_command = 'git show --pretty="format:%%ae" --name-only %s' % commit_git
            modified_files = command(str_command)
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
                    artifact = dict_artifact[path_directory]
                    if artifact not in list_artifact:
                        list_artifact.append(artifact)
            print(list_artifact)
            if branch in dict_branch:
                ls_branch_artifact = dict_branch[branch]
            else:
                ls_branch_artifact = []
            for artifact in list_artifact:
                dict = {'artifact': artifact, 'email': email, 'type_tech': type_tech}
                ls_branch_artifact.append(dict)
            dict_branch[branch] = ls_branch_artifact

        print dict_branch

        result_pull = 'do pull'  # command('git pull')
        print(result_pull)
