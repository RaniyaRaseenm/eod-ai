import random
import math
from pydantic import BaseModel
from typing import Optional, List

# Pydantic typed models
class Observation(BaseModel):
    agent_position: list
    grid_size: int
    bombs_found: list
    bombs_defused: list
    current_bomb_index: Optional[int] = None
    scan_done: bool
    hint: Optional[str] = None
    time_left: int
    steps: int
    done: bool
    total_reward: float
    distance_to_bomb: int
    nearest_bomb_position: Optional[list] = None
    last_action: Optional[str] = None

class Action(BaseModel):
    action: str

class Reward(BaseModel):
    reward: float

class EODEnvironment:
    ACTIONS = [
        "move_up", "move_down", "move_left", "move_right",
        "scan", "cut_red", "cut_blue", "cut_green"
    ]

    WIRES = ["red", "blue", "green"]

    def __init__(self, grid_size=8, timer=30, hint_accuracy=1.0, num_bombs=1):
        self.grid_size = grid_size
        self.timer = timer
        self.hint_accuracy = hint_accuracy
        self.num_bombs = num_bombs
        self.reset()

    def reset(self):
        self.agent_pos = [0, 0]
        self.bombs = []
        for _ in range(self.num_bombs):
            while True:
                pos = [
                    random.randint(0, self.grid_size - 1),
                    random.randint(0, self.grid_size - 1)
                ]
                if pos != self.agent_pos and pos not in self.bombs:
                    self.bombs.append(pos)
                    break

        self.correct_wires = [random.choice(self.WIRES) for _ in self.bombs]
        self.found_bombs = [False] * self.num_bombs
        self.defused_bombs = [False] * self.num_bombs
        self.time_left = self.timer
        self.steps = 0
        self.done = False
        self.current_bomb_index = None
        self.scan_done = False
        self.hint = None
        self.last_action = None
        self.total_reward = 0
        return self.get_state()

    def _distance_to_nearest_bomb(self):
        unfound = [
            self.bombs[i] for i in range(self.num_bombs)
            if not self.found_bombs[i]
        ]
        if not unfound:
            return 0
        distances = [
            abs(self.agent_pos[0] - b[0]) + abs(self.agent_pos[1] - b[1])
            for b in unfound
        ]
        return min(distances)

    def _get_nearest_bomb_position(self):
        unfound = [
            self.bombs[i] for i in range(self.num_bombs)
            if not self.found_bombs[i]
        ]
        if not unfound:
            return None
        return min(unfound, key=lambda b: abs(self.agent_pos[0]-b[0]) + abs(self.agent_pos[1]-b[1]))

    def _get_hint(self, bomb_index):
        correct = self.correct_wires[bomb_index]
        return f"cut {correct}"

    def step(self, action):
        if self.done:
            return self.get_state(), 0, True, {}

        reward = -1
        self.steps += 1
        self.time_left -= 1
        self.last_action = action
        prev_distance = self._distance_to_nearest_bomb()

        if action == "move_up":
            if self.agent_pos[0] > 0:
                self.agent_pos[0] -= 1
        elif action == "move_down":
            if self.agent_pos[0] < self.grid_size - 1:
                self.agent_pos[0] += 1
        elif action == "move_left":
            if self.agent_pos[1] > 0:
                self.agent_pos[1] -= 1
        elif action == "move_right":
            if self.agent_pos[1] < self.grid_size - 1:
                self.agent_pos[1] += 1

        if action in ["move_up", "move_down", "move_left", "move_right"]:
            new_distance = self._distance_to_nearest_bomb()
            if new_distance < prev_distance:
                reward += 2
            elif new_distance > prev_distance:
                reward -= 2

        for i, bomb in enumerate(self.bombs):
            if self.agent_pos == bomb and not self.found_bombs[i]:
                self.found_bombs[i] = True
                self.current_bomb_index = i
                self.scan_done = False
                self.hint = None
                reward += 50

        if action == "scan":
            if self.current_bomb_index is not None and not self.scan_done:
                self.scan_done = True
                self.hint = self._get_hint(self.current_bomb_index)
                reward += 5
            else:
                reward -= 5

        if action in ["cut_red", "cut_blue", "cut_green"]:
            wire = action.split("_")[1]
            if self.current_bomb_index is not None:
                correct = self.correct_wires[self.current_bomb_index]
                if wire == correct:
                    self.defused_bombs[self.current_bomb_index] = True
                    reward += 100
                    self.current_bomb_index = None
                    self.scan_done = False
                    self.hint = None
                    if all(self.defused_bombs):
                        self.done = True
                        reward += 50 * self.time_left
                else:
                    reward -= 100
                    self.done = True
            else:
                reward -= 10

        if self.time_left <= 0:
            self.done = True
            reward -= 50

        self.total_reward += reward
        return self.get_state(), reward, self.done, {}

    def get_state(self):
        return {
            "agent_position": self.agent_pos.copy(),
            "grid_size": self.grid_size,
            "bombs_found": self.found_bombs.copy(),
            "bombs_defused": self.defused_bombs.copy(),
            "current_bomb_index": self.current_bomb_index,
            "scan_done": self.scan_done,
            "hint": self.hint,
            "time_left": self.time_left,
            "steps": self.steps,
            "done": self.done,
            "total_reward": self.total_reward,
            "distance_to_bomb": self._distance_to_nearest_bomb(),
            "nearest_bomb_position": self._get_nearest_bomb_position(),
            "last_action": self.last_action
        }

    def render(self):
        print(f"\n{'='*20}")
        print(f"Time Left: {self.time_left} | Steps: {self.steps} | Reward: {self.total_reward}")
        print(f"{'='*20}")
        for r in range(self.grid_size):
            row = ""
            for c in range(self.grid_size):
                pos = [r, c]
                if pos == self.agent_pos:
                    row += "A "
                elif pos in self.bombs:
                    i = self.bombs.index(pos)
                    if self.defused_bombs[i]:
                        row += "✓ "
                    elif self.found_bombs[i]:
                        row += "B "
                    else:
                        row += ". "
                else:
                    row += ". "
            print(row)
        if self.hint:
            print(f"Hint: {self.hint}")
        print(f"{'='*20}\n")