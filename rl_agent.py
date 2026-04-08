from tasks import get_task
from grader import grade


def rl_agent(env):
    state = env.reset()

    tried_wires = {}

    grid = state["grid_size"]

    # Precompute full grid path (snake pattern)
    path = []
    for i in range(grid):
        row = list(range(grid))
        if i % 2 == 1:
            row.reverse()
        for j in row:
            path.append((i, j))

    path_index = 0

    while not state["done"]:

        x, y = state["agent_position"]

        # =====================
        # ON BOMB
        # =====================
        if state["current_bomb_index"] is not None:
            bomb_id = state["current_bomb_index"]

            if bomb_id not in tried_wires:
                tried_wires[bomb_id] = []

            # always scan first
            if not state["scan_done"]:
                action = "scan"

            else:
                # since accuracy = 1.0 → trust hint
                hint = state.get("hint", "").lower()

                if "red" in hint:
                    action = "cut_red"
                elif "blue" in hint:
                    action = "cut_blue"
                elif "green" in hint:
                    action = "cut_green"
                else:
                    action = "cut_red"

        # =====================
        # MOVEMENT (SYSTEMATIC)
        # =====================
        else:
            target = path[path_index]

            if (x, y) == target:
                path_index += 1
                if path_index >= len(path):
                    path_index = len(path) - 1
                target = path[path_index]

            tx, ty = target

            if x < tx:
                action = "move_down"
            elif x > tx:
                action = "move_up"
            elif y < ty:
                action = "move_right"
            elif y > ty:
                action = "move_left"
            else:
                action = "move_right"

        state, reward, done = env.step(action)

    return state


# ======================
# MAIN
# ======================
if __name__ == "__main__":

    print("\n🚀 FINAL FIXED AGENT...\n")

    for task in ["task1", "task2", "task3"]:
        grade(task, rl_agent)