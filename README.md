---
title: eod-ai
sdk: docker
emoji: 🔥
colorFrom: blue
colorTo: red
---

# EOD-AI: Bomb Disposal Training Simulator

> Training an AI to defuse bombs — so humans don't have to

## 🚨 Problem Statement

In high-risk environments such as bomb disposal zones, disaster sites, and search-and-rescue operations, human intervention is extremely dangerous and often life-threatening. 

Traditional approaches rely heavily on manual inspection or remote-controlled systems, which:
- Lack real-time intelligence
- Require constant human supervision
- Are prone to human error under stress

There is a critical need for intelligent systems that can:
- Autonomously explore unknown environments  
- Analyze risk using real-time feedback  
- Make safe and optimal decisions without direct human control

 ## ❓ Why This Problem?

This problem was chosen because it directly impacts **human safety and emergency response efficiency**.

Real-world inspiration comes from:
- Explosive Ordnance Disposal (EOD) operations  
- Disaster response scenarios (earthquakes, collapsed structures)  
- Military and defense applications  

Even today, bomb disposal robots exist, but many are:
- Remotely controlled (not intelligent)
- Limited in adaptability
- Dependent on human decisions  

Our goal is to move from:
➡️ *Remote-controlled systems*  
➡️ to *Autonomous intelligent agents*

This shift can significantly:
- Reduce human risk  
- Improve response time  
- Enable scalable deployment in dangerous zones

## What is this project?
EOD-AI is a reinforcement learning environment where an LLM agent learns 
to find and defuse bombs in a grid world. Built for the OpenENV Hackathon 
by Meta, HuggingFace and PyTorch.

## How it works
1. Agent searches an 8x8 grid for hidden bombs
2. Agent scans the bomb to get a wire hint
3. LLM brain reads the situation and decides which wire to cut
4. Right wire = success, Wrong wire = explosion!

## 3 Difficulty Levels
| Level | Timer | Hint Accuracy | Bombs |
|---|---|---|---|
| Task 1 (Easy) | 30s | 100% correct | 1 |
| Task 2 (Medium) | 20s | 70% correct | 1 |
| Task 3 (Hard) | 15s | 30% correct | 2 |

## Reward System
| Action | Reward |
|---|---|
| Move closer to bomb | +2 |
| Move away from bomb | -2 |
| Find bomb | +50 |
| Scan bomb | +5 |
| Cut correct wire | +100 |
| Cut wrong wire | -100 |
| Each step | -1 |

## 📁 Project Structure

- app.py → Main application entry point
- train.py → Used for training the model
- test.py → Used for testing functionality
- inference.py → Runs model inference (prediction)
- tasks.py → Defines tasks for the system
- grader.py → Evaluates results
- rl_agent.py → agent learning logic
- eod_env.py → Environment setup
- openenv.yaml → Environment configuration
- Dockerfile → Container setup
- README.md → Project documentation

## 🔐 Environment Variables

This project uses API tokens for authentication.

Set the following environment variables before running:

- HF_TOKEN = your Hugging Face token
- API_BASE_URL = https://router.huggingface.co/v1

⚠️ Do NOT hardcode tokens in the code.

## 🎮 Role of Unity (Visualization Engine)

While the backend handles intelligence, **Unity transforms abstract AI decisions into a real-world simulation**.

Unity enables:

### 🌍 Real-Time Environment Simulation
- 2D logic → converted into immersive 3D space  
- Grid-based navigation becomes spatial movement  

### 🧠 Visual Intelligence Representation
- Signal strength shown via color transitions (low → high)  
- Agent behavior becomes observable and interpretable  

### 🎯 Phase-Based Visualization
- Search → Analyze → Defuse shown as distinct stages  
- Enhances understanding of decision flow  

### 🎥 Enhanced Demonstration
- Converts logs into **cinematic, interactive experience**  
- Makes the system intuitive for non-technical users  
➡️ Unity bridges the gap between:
**AI reasoning → Human understanding**
  
<img src="https://github.com/user-attachments/assets/68158b39-8246-4bc1-b505-5824ea26d876" width="400"/>


## Sample Output
<img width="400" height="637" alt="Screenshot 2026-04-08 221544" src="https://github.com/user-attachments/assets/10e17e7b-7816-4a1e-b783-b1e26538b6ed" />
<img width="500" height="334" alt="Screenshot 2026-04-08 221600" src="https://github.com/user-attachments/assets/6df4df99-4947-4ab1-a90a-698b999b5b6c" />

🤖 EOD-AI agent successfully defusing bombs across all 3 difficulty levels!
The agent navigates the grid, scans bombs, and uses an LLM to decide which wire to cut.
Task 1: 0.900 | Task 2: 0.865 | Task 3: 0.760 — all tasks completed with success! 💣✅

## Environmental Application
This system can be extended to:

- 💣 Bomb Detection & Disposal (EOD operations)  
- 🚑 Disaster Response (earthquake, fire rescue)  
- 🛰️ Search & Rescue Missions  
- 🏭 Industrial Hazard Monitoring  
- 🛡️ Defense & Security Systems  

The core idea is to deploy *autonomous agents in environments where humans should not go* .

## Project Video Demonstration

https://github.com/user-attachments/assets/d0547a2c-859f-4985-9bc2-64a10ca467e9

## Live Demo
🤗 [Hugging Face Space](https://huggingface.co/spaces/raniyraseenm/eod-ai)
Try the live EOD-AI agent defusing bombs in real time across 3 difficulty levels!

## Action Space
move_up, move_down, move_left, move_right, scan, cut_red, cut_blue, cut_green

## Observation Space
agent_position, bombs_found, bombs_defused, hint, time_left, steps, done

## How to Run
```bash
pip install openai numpy fastapi uvicorn openenv-core
python inference.py
Tech Stack
Python 3.12
HuggingFace API (Llama 3.1)
OpenENV framework
Docker
HuggingFace Spaces

