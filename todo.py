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
        self._directory = os.path.join(os.path.expanduser('~'), '.config', 'todo')
        self._filepath = os.path.join(self._directory, '.todo')
        self._open_file()
        self._task_number = self._tasks[0] + 1

    def print_tasks(self):
        if self._fname.closed :
            self._open_file()
        for task in self._tasks[1:]:
            print (task)
        json.dump(self.json(), self._fname)
        self._fname.close()

    def add(self, arg):
        if self._fname.closed :
            self._open_file()
        self._tasks[0] += 1
        entry_number = self._tasks[0]
        self._tasks.append(Task(self._task_number, arg))
        json.dump(self.json(), self._fname)
        self._fname.close()

    def _open_file(self):
        self._tasks = []
        if not os.path.exists(self._directory):
            os.makedirs(self._directory)
            self._tasks = [0]
        elif not os.path.exists(self._filepath):
            self._tasks = [0]
            self.fname = open(self._filepath, 'w+')
        else:
            self._fname = open(self._filepath, 'a+')
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
        self._fname = open(self._filepath, 'w+')


    def remove(self, args):
        t = self._find_task(args)
        self._tasks.remove(t)
        json.dump(self.json(), self._fname)
        self._fname.close()


    def check_status(self, args):
        t = self._find_index(args)
        return self._tasks[t].complete

    def completed(self, args):
        t = self._find_index(args)
        self._tasks[t].complete = True

    def _find_task(self, args):
        for t in self._tasks[1:]:
            if t.task_id == int(args):
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
    parser.add_argument("-r", "--remove", help = "remove a task")
    parser.add_argument("-l", "--list", action = "store_true", help = "print tasks list")
    args = parser.parse_args()
    if args.add:
        job.add(args.add)
        job.print_tasks()
    elif args.remove:
        job.remove(args.remove)
        print("List of tasks")
        job.print_tasks()
    elif args.list:
        job.print_tasks()
