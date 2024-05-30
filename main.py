import queue
import threading
import psutil
from enum import Enum
from functions import Functions

class ProcessControllerStates(Enum):
    NOT_STARTED = 0
    RUNNING = 1
    STOPPING = 2
    STOPPED = 3

class ProcessController:
    def __init__(self, max_threads=5):
        self._queue = queue.Queue()
        self._threads = []
        self._max_threads = max_threads
        self._state = ProcessControllerStates.NOT_STARTED
        self._max_proc = 1
        self._max_exec_time = 5
        self._semaphore = threading.Semaphore(self._max_proc)
        self._lock = threading.Lock()
        self._alive_tasks_num = 0
        self._tasks_num = 0
        self._cpu_usage = 0.0

    def set_max_proc(self, n):
        self._max_proc = n
        self._semaphore = threading.Semaphore(self._max_proc)

    def set_max_exec_time(self, n):
        self._max_exec_time = n

    def start(self, tasks, max_exec_time=5):
        self._max_exec_time = max_exec_time
        self._state = ProcessControllerStates.RUNNING
        for task, args in tasks:
            self.submit(task, args)
        for _ in range(self._max_threads):
            t = threading.Thread(target=self._worker)
            t.daemon = True
            t.start()
            self._threads.append(t)

    def submit(self, task, args):
        self._queue.put((task, args))
        self._tasks_num += 1

    def wait(self, timeout=None):
        self._state = ProcessControllerStates.STOPPING
        for t in self._threads:
            t.join(timeout)
        self._state = ProcessControllerStates.STOPPED

    def wait_count(self):
        return self._tasks_num

    def alive_count(self):
        return self._alive_tasks_num

    def _worker(self):
        while True:
            task, args = self._queue.get()
            self._alive_tasks_num += 1
            try:
                self._semaphore.acquire()
                task(*args)
            except Exception as e:
                print(f"Error executing task: {e}")
            finally:
                self._semaphore.release()
                self._alive_tasks_num -= 1
                self._tasks_num -= 1
                self._queue.task_done()

    def _monitor_cpu_usage(self):
        while True:
            self._cpu_usage = psutil.cpu_percent(interval=1)
            print(f"CPU usage: {self._cpu_usage:.2f}%")

    def start_cpu_monitoring(self):
        t = threading.Thread(target=self._monitor_cpu_usage)
        t.daemon = True
        t.start()

if __name__ == '__main__':

    f = Functions()
    tasks = [
        (f.functionMultiply, (10, 3)),
        (f.functionMultiply, (1, 3)),
        (f.function1Summ, (1, 10, 3)),
        (f.function1Summ, (1, 1, 4)),
        (f.functionOne, (2,)),
        (f.functionOne, (1,))
    ]

    controller = ProcessController()
    controller.set_max_proc(2)
    controller.start(tasks, 5)
    controller.start_cpu_monitoring()

    print("Waiting for tasks to complete...")
    controller.wait(timeout=5)
    print("All tasks completed!")

    print("Tasks left to run:", controller.wait_count())
    print("Currently running tasks:", controller.alive_count())
    print("CPU usage:", controller._cpu_usage)

