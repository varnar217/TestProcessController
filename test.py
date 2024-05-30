import pytest
from main import ProcessController, ProcessControllerStates

from functions import Functions

@pytest.fixture
def process_controller():
    return ProcessController()

@pytest.fixture
def functions():
    return Functions()

def test_process_controller_init(process_controller):
    assert process_controller._state == ProcessControllerStates.NOT_STARTED
    assert process_controller._max_threads == 5
    assert process_controller._max_proc == 1
    assert process_controller._max_exec_time == 5

def test_set_max_proc(process_controller):
    process_controller.set_max_proc(2)
    assert process_controller._max_proc == 2

def test_set_max_exec_time(process_controller):
    process_controller.set_max_exec_time(10)
    assert process_controller._max_exec_time == 10

def test_start(process_controller, functions):
    tasks = [
        (functions.functionMultiply, (1, 1)),
        (functions.functionMultiply, (1, 3)),
        (functions.function1Summ, (1, 10, 3)),
        (functions.function1Summ, (1, 1, 4)),
        (functions.functionOne, (2,)),
        (functions.functionOne, (1,))
    ]
    process_controller.start(tasks, 5)
    assert process_controller._state == ProcessControllerStates.RUNNING

def test_submit(process_controller):
    task = lambda x, y: x + y
    process_controller.submit(task, (1, 2))
    assert process_controller._tasks_num == 1

def test_wait(process_controller):
    process_controller.wait(timeout=30)
    assert process_controller._state == ProcessControllerStates.STOPPED

def test_wait_count(process_controller):
    assert process_controller.wait_count() == 0

def test_alive_count(process_controller):
    assert process_controller.alive_count() == 0