---
title: eod-ai
sdk: docker
emoji: 🔥
colorFrom: blue
colorTo: red
---

# EOD-AI: Bomb Disposal Training Simulator

> Training an AI to defuse bombs — so humans don't have to

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

## How to Run
```bash
pip install openai numpy openenv
python inference.py
Tech Stack
Python 3.12
HuggingFace API (Llama 3.1)
OpenENV framework
Docker
HuggingFace Spaces



