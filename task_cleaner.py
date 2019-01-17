#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, getopt, os, shutil
from subprocess import Popen, PIPE
from redmine_caller import RedmineCaller
import asyncio

help_str = '''This is script for clean logs, config folders with some tasks of redmine.
It get readmine task number, check status on server and remove folder (files) if task is closed.
Parameters:
    -s (--server) address of redmine server
    -u (--user) redmine user name. This is requaired parameter
    -p (--password) redmine password name. This is requaired parameter
    -f (--folder) folder list to cleanup
    -g (--git) flag shows that need to clean git repo in folder
Example:
task_cleaner -s red.some_serv.com -u user -p password -f '/tmp/logs,/tmp/configs,/tmp/code' -g
'''

def parce_arguments(argv):
    result = [default_server, None, None, None, False]
    try:
        opts, _ = getopt.getopt(argv,"s:u:p:f:g",
            ["server=", "user", "password", "folder", "git"])
    except getopt.GetoptError:
        print(help_str)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_str)
            sys.exit()
        elif opt in ("-s", "--server"):
            result[0] = arg
        elif opt in ("-u", "--user"):
            result[1] = arg
        elif opt in ("-p", "--password"):
            result[2] = arg
        elif opt in ("-f", "--folder"):
            result[3] = arg
        elif opt in ("-g", "--git"):
            result[4] = True
    return result

def extract_task_id_from_str(folder_name):
    result = folder_name.split('_')[0]
    if result.isdigit():
        return result
    return None

class FoldersCleaner:
    def __init__(self):
        pass

    def getResourcesToClean(self):
        result = []
        subdirs = (filename for filename in os.listdir('.') if os.path.isdir(filename))
        for subdir in subdirs:
            # print ('subdir name {}'.format(subdir))
            task_id = extract_task_id_from_str(subdir)
            if task_id == None:
                continue
            result.append((task_id, subdir))
        return result

    def removeResource(self, resource):
        shutil.rmtree(resource)

class GitCleaner:
    def __init__(self):
        pass

    def execute_command(self, command):
        proc = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        proc.wait()
        return proc.communicate()[0]

    def getResourcesToClean(self):
        result = []
        branches = self.execute_command("git branch").decode().split('\n')
        for branch in branches:
            fixed_branch = branch.strip('\t *')
            task_id = extract_task_id_from_str(fixed_branch)
            if task_id == None:
                continue
            result.append((task_id, fixed_branch))
        return result

    def removeResource(self, resource):
        # ToDo. Add async there too
        self.execute_command("git branch -D " + resource)

async def clean_task(cleaner, issue, resource):
    if await test_worker.is_issue_closed(issue):
        print ('need to remove resource {}'.format(resource))
        cleaner.removeResource(resource)

def clean(cleaner):
    clean_coroutines = [clean_task(cleaner, issue, resource)
                        for issue, resource in cleaner.getResourcesToClean()]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(clean_coroutines))
    loop.close()

if __name__ == "__main__":
    address, user, password, dir_list, git_flag = parce_arguments(sys.argv[1:])

    if None == user or None == password:
        print('You need to specify user and password for redmine server.')
        print(help_str)
        sys.exit()

    if None == dir_list:
        print('You need to specify dirs to cleanup.')
        print(help_str)
        sys.exit()

    test_worker = RedmineCaller(address, user, password)

    current_dir = os.getcwd()

    if True != git_flag:
        cleaner = FoldersCleaner()
    else:
        cleaner = GitCleaner()

    for dir in dir_list.split(','):
        print ('Going to cleanup dir {}'.format(dir))
        os.chdir(dir)

        clean(cleaner)
        # subdirs = (filename for filename in os.listdir('.') if os.path.isdir(filename))
        # for subdir in subdirs:
        #     # print ('subdir name {}'.format(subdir))
        #     task_id = extract_task_id_from_dir_name(subdir)
        #     if task_id == None:
        #         continue
        #     # print ('looking for a task {}'.format(task_id))
        #     if test_worker.is_issue_closed(task_id):
        #         shutil.rmtree(subdir)
        #         print ('need to remove dir {}'.format(subdir))

    os.chdir(current_dir)

