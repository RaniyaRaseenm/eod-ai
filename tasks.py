from eod_env import EODEnvironment

def task1():
    return EODEnvironment(
        grid_size=8,
        timer=30,
        hint_accuracy=1.0,
        num_bombs=1
    )

def task2():
    return EODEnvironment(
        grid_size=8,
        timer=25,
        hint_accuracy=0.7,
        num_bombs=1
    )

def task3():
    return EODEnvironment(
        grid_size=8,
        timer=20,
        hint_accuracy=0.3,
        num_bombs=2
    )

TASKS = {
    "task1": task1,
    "task2": task2,
    "task3": task3
}

def get_task(name):
    if name not in TASKS:
        raise ValueError(f"Unknown task: {name}")
    return TASKS[name]()