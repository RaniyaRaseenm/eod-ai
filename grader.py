from tasks import get_task

def grade(task_name, run_fn):
    """
    Grade a task run.
    Returns a score between 0.0 and 1.0
    
    run_fn: a function that takes an env and returns final state
    """
    env = get_task(task_name)
    state = env.reset()

    # Run the agent
    final_state = run_fn(env)

    score = 0.0

    # Did it find the bomb? (20% of score)
    bombs_found = sum(final_state["bombs_found"])
    total_bombs = env.num_bombs
    score += 0.2 * (bombs_found / total_bombs)

    # Did it defuse the bomb? (50% of score)
    bombs_defused = sum(final_state["bombs_defused"])
    score += 0.5 * (bombs_defused / total_bombs)

    # Time remaining bonus (20% of score)
    time_ratio = final_state["time_left"] / env.timer
    if bombs_defused == total_bombs:
        score += 0.2 * time_ratio

    # Efficiency bonus (10% of score)
    max_steps = env.timer
    steps_used = final_state["steps"]
    if bombs_defused == total_bombs:
        efficiency = max(0, 1 - (steps_used / max_steps))
        score += 0.1 * efficiency

    # Clamp between 0.0 and 1.0
    score = round(min(1.0, max(0.0, score)), 4)

    print(f"\n{'='*30}")
    print(f"Task: {task_name}")
    print(f"Bombs Found: {bombs_found}/{total_bombs}")
    print(f"Bombs Defused: {bombs_defused}/{total_bombs}")
    print(f"Time Left: {final_state['time_left']}s")
    print(f"Steps Used: {steps_used}")
    print(f"Final Score: {score}")
    print(f"{'='*30}\n")

    return score


# ✅ SMART AGENT (REPLACES RANDOM)
def smart_agent(env):
    state = env.reset()
    
    tried_wires = set()
    
    while not state["done"]:
        
        # If on bomb
        if state["current_bomb_index"] is not None:
            
            # Step 1: Scan
            if not state["scan_done"]:
                action = "scan"
            
            else:
                hint = state["hint"]
                
                # Step 2: Use hint (avoid wrong wire)
                possible_wires = ["red", "blue", "green"]
                
                if hint:
                    for w in possible_wires:
                        if f"not {w}" in hint:
                            possible_wires.remove(w)
                            break
                
                # Step 3: Try remaining wires safely
                for wire in possible_wires:
                    if wire not in tried_wires:
                        action = f"cut_{wire}"
                        tried_wires.add(wire)
                        break
                else:
                    action = "cut_red"  # fallback
        
        else:
            # Move towards bomb using simple pattern
            x, y = state["agent_position"]
            grid = state["grid_size"]
            
            if x < grid - 1:
                action = "move_down"
            elif y < grid - 1:
                action = "move_right"
            else:
                action = "move_up"
        
        state, reward, done = env.step(action)
    
    return state


if __name__ == "__main__":
    
    for task in ["task1", "task2", "task3"]:
        grade(task, smart_agent)