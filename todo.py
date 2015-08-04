import argparse
import json
from datetime import datetime
import os


class Task:

    def __init__(self, task_id, job, time = datetime.now(), completed = False):
        self.task_id  = task_id
        self.job      = job
        self.time     = time
        self.complete = completed

    def __str__(self):
        return str(self.task_id) + ". " + self.job + "\t" + str(self.time)

class Job:

    def __init__(self):
        directory = os.path.join(os.path.expanduser('~'), '.config', 'todo')
        filepath = os.path.join(directory, '.todo')
        self._fname = None
        self._tasks = []
        if not os.path.exists(directory):
            os.makedirs(directory)
            self._tasks = [0]
        elif not os.path.exists(filepath):
            self._tasks = [0]
            self.fname = open(filepath, 'w+')
        else:
            self._fname = open(filepath, 'r')
        if not self._tasks:
            try:
                # error is possible in json.load if fname is empty
                data = json.load(self._fname)
                self._tasks = [data[0]]
                # converting all the string versions of the tasks to
                # Task instances
                for task_str in data[1:]:
                    task_id, job, time, complete = task_str
                    time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
                    self._tasks.append(Task(task_id, job, time, complete))
            except ValueError:
                self._tasks = [0]
        self._task_number = self._tasks[0] + 1
        self._fname = open(filepath, 'r+')

    def print_tasks(self):
        for task in self._tasks[1:]:
            print (task)

    def add(self, arg):
        self._tasks[0] += 1
        entry_number = self._tasks[0]
        self._tasks.append(Task(self._task_number, arg))
        json.dump(self.json(), self._fname)
        self._fname.close()

    def remove(self, args):
        t = self._find_index(args)
        self._tasks.remove(t)

    def check_status(args):
        t = self._find_index(args)
        return self._tasks[t].status

    def completed(args):
        t = self._find_index(args)
        self._tasks[t].status = True

    def _find_index(args):
        for t in self._tasks:
            if t.task_id == args:
                return t

    def json(self):
        lst = []
        lst.append(self._tasks[0])
        for task in self._tasks[1:]:
            x = [task.task_id, task.job, str(task.time), task.complete]
            lst.append(x)
        return lst

if __name__ == '__main__':
    job = Job()
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--add", help = "add a task")
    args = parser.parse_args()
    if args.add:
        job.add(args.add)
        job.print_tasks()
