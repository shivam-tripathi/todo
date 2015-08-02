import argparse
import json
from datetime import datetime

parser = argparse.ArgumentParser(description = 'Arguments for to-do list')
parser.add_argument('add', )
parser.add_argument('todo', action = 'store_true')
parser.add_argument()


class Task :

    def __init__(self, task_id, job):
        self.task_id = task_id
        self.job     = job
        self.time    = datetime.now()
        self.status  = 'complete'

class Job :

    def __init__(self):
        self._fname = open('.todo', 'r+')
        self._tasks = json.load(self._fname)
        self._task_number = self._tasks[0]
        self._fname.close()

    def print_tasks(self):
        for i in range(1,self._task_number):
            print (self._tasks[i])

    def add(self, arg):
        self._tasks[0] += 1
        entry_number = self._tasks[0]
        self._tasks.append( Task(self._task_number, arg)
        self._fname = open('.todo', 'r+')
        json.dump(self._tasks, self._fname)

    def remove(self, args):
        t = self._find_index(args)
        self._tasks.remove(t)

    def check_status(args):
        t = self._find_index(args)
        return self._tasks[t].status

    def completed(args):
        t = self._find_index(args)
        self._tasks[t].status = 'complete'

    def _find_index(args):
        for t in self._tasks:
            if t.task_id == args:
                return t



test = Job()
test.add("trial input")
test.print_tasks()
