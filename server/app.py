from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import threading
from inference import run_agent
from tasks import get_task
from eod_env import EODEnvironment

app = FastAPI()
results = {}
env = get_task("task1")  # default env

@app.post("/reset")
def reset():
    state = env.reset()
    return state

@app.post("/step")
def step(action: dict):
    state, reward, done = env.step(action["action"])
    return {"state": state, "reward": reward, "done": done}

@app.get("/state")
def state():
    return env.get_state()

@app.get("/", response_class=HTMLResponse)
def home():
    html = """
    <html>
    <head><title>EOD-AI Bomb Disposal</title></head>
    <body style="font-family:Arial; padding:20px; background:#1a1a2e; color:white">
    <h1>💣 EOD-AI Bomb Disposal Simulator</h1>
    <p>Training an AI to defuse bombs so humans don't have to!</p>
    <h2>Results:</h2>
    """
    for task, data in results.items():
        html += f"<p>✅ {task}: Defused {data['bombs_defused']} bombs | Time left: {data['time_left']}s | Steps: {data['steps']}</p>"
    if not results:
        html += "<p>🔄 Running tasks... refresh in 1 minute!</p>"
    html += "</body></html>"
    return html

@app.on_event("startup")
def startup():
    def run_tasks():
        for task_name in ["task1", "task2", "task3"]:
            e = get_task(task_name)
            final_state, rewards, steps_taken = run_agent(e)
            bombs_defused = sum(final_state["bombs_defused"])
            total_bombs = e.num_bombs
            results[task_name] = {
                "bombs_defused": f"{bombs_defused}/{total_bombs}",
                "time_left": final_state["time_left"],
                "steps": final_state["steps"]
            }
    thread = threading.Thread(target=run_tasks)
    thread.daemon = True
    thread.start()
    
def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()