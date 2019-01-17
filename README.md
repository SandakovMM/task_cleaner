This is script for clean logs, config folders with some tasks of redmine.
It get readmine task number, check status on server and remove folder (files) if task is closed.

### Parameters:
1. -s (--server) address of redmine server
2. -u (--user) redmine user name. This is requaired parameter
3. -p (--password) redmine password name. This is requaired parameter
4. -f (--folder) folder list to cleanup
5. -g (--git) flag shows that need to clean git repo in folder

Example:
task_cleaner -s red.some_serv.com -u user -p password -f '/tmp/logs,/tmp/configs,/tmp/code' -g

