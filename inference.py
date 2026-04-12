import os
import textwrap
from typing import List, Optional
from openai import OpenAI
from tasks import get_task
from grader import grade

# Competition required variables
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
API_KEY = os.getenv("API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME") or "meta-llama/Llama-3.1-8B-Instruct"

BENCHMARK = "eod-ai"
MAX_STEPS = 200

# Competition required: use OpenAI client
try:
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=API_KEY or HF_TOKEN
    )
except Exception as e:
    print(f"[DEBUG] Client error: {e}", flush=True)
    client = None

# Competition required log formats
def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}", flush=True)

def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)

def get_llm_action(state: dict) -> str:
    hint = state.get("hint", "")

    # Use hint directly if available
    if hint:
        if "cut red" in hint:
            return "cut_red"
        elif "cut blue" in hint:
            return "cut_blue"
        elif "cut green" in hint:
            return "cut_green"

    # Use LLM as backup
    try:
        if client is None:
            return "cut_red"

        prompt = textwrap.dedent(f"""
            You are a bomb disposal expert.
            Hint: {state.get('hint', 'no hint')}
            Choose one: cut_red, cut_blue, cut_green
            Reply with ONLY the action name.
        """).strip()

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Reply with exactly one action name only."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=10,
            temperature=0.1
        )
        action = response.choices[0].message.content.strip().lower()
        valid = ["cut_red", "cut_blue", "cut_green"]
        if action in valid:
            return action
    except Exception as e:
        print(f"[DEBUG] LLM error: {e}", flush=True)

    return "cut_red"

def smart_move(state: dict) -> str:
    agent = state["agent_position"]
    bomb = state.get("nearest_bomb_position")

    if bomb is None:
        return "move_right"

    ar, ac = agent
    br, bc = bomb

    if ar < br:
        return "move_down"
    elif ar > br:
        return "move_up"
    elif ac < bc:
        return "move_right"
    elif ac > bc:
        return "move_left"
    return "scan"

def run_agent(env):
    state = env.reset()
    rewards = []
    steps_taken = 0

    while not state["done"] and steps_taken < MAX_STEPS:
        if state["current_bomb_index"] is None:
            action = smart_move(state)
        elif not state["scan_done"]:
            action = "scan"
        else:
            action = get_llm_action(state)
        state, reward, done, info= env.step(action)
        rewards.append(reward)
        steps_taken += 1

        log_step(
            step=steps_taken,
            action=action,
            reward=reward,
            done=done,
            error=None
        )

    return state, rewards, steps_taken

def run_task(task_name: str):
    env = get_task(task_name)
    log_start(task=task_name, env=BENCHMARK, model=MODEL_NAME)

    rewards = []
    steps_taken = 0
    score = 0.0
    success = False

    try:
        final_state, rewards, steps_taken = run_agent(env)

        bombs_defused = sum(final_state["bombs_defused"])
        total_bombs = env.num_bombs
        time_ratio = final_state["time_left"] / env.timer

        score = 0.0
        score += 0.2 * (sum(final_state["bombs_found"]) / total_bombs)
        score += 0.5 * (bombs_defused / total_bombs)
        if bombs_defused == total_bombs:
            score += 0.2 * time_ratio
            efficiency = max(0, 1 - (steps_taken / env.timer))
            score += 0.1 * efficiency
        score = round(min(1.0, max(0.0, score)), 3)
        success = bombs_defused == total_bombs

    except Exception as e:
        print(f"[ERROR] {task_name} failed: {e}", flush=True)

    finally:
        log_end(
            success=success,
            steps=steps_taken,
            score=score,
            rewards=rewards
        )

    return score

if __name__ == "__main__":
    print("🚀 EOD-AI Inference", flush=True)
    for task in ["task1", "task2", "task3"]:
        print(f"\n--- {task} ---", flush=True)
        try:
            run_task(task)
        except Exception as e:
            print(f"[ERROR] {task} failed: {e}", flush=True)