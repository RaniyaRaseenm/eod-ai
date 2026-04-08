from tasks import get_task
from inference import run_agent

print("Running task1...")
env1 = get_task("task1")
print(run_agent(env1))

print("Running task2...")
env2 = get_task("task2")
print(run_agent(env2))

print("Running task3...")
env3 = get_task("task3")
print(run_agent(env3))