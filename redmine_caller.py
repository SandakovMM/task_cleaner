#!/usr/bin/python3
# -*- coding: utf-8 -*-
from redminelib import Redmine
import asyncio
from concurrent.futures import ThreadPoolExecutor

class RedmineCaller:
    def __init__(self, addr, username, password):
        self.redmine_call_executor = ThreadPoolExecutor(4)
        self.server_address = addr
        self.redmine_server = Redmine(addr, username=username, password=password)
        self.projects = {}
        self.opened_issues = {}

    def open_project(self, project_name):
        self.projects['project_name'] = self.redmine_server.project.get(project_name)


    async def is_issue_closed(self, id):
        issue = self.opened_issues.get(id)
        if (None == issue):
            loop = asyncio.get_event_loop()
            # issue = await loop.run_in_executor(self.redmine_call_executor,
            #                                    self.redmine_server.issue.get, id)
            self.opened_issues['id'] = issue = self.redmine_server.issue.get(id)
            self.opened_issues['id'] = issue

        issue_status = getattr(issue, "status")
        print ("for issue {} status id {}".format(id, issue_status))
        return "Closed" == issue_status.name or "Rejected" == issue_status.name


if __name__ == "__main__":
    caller = RedmineCaller('http://red.eltex.loc', 'michail.sandakov', '3LefN2')
    caller.is_issue_closed(113429)