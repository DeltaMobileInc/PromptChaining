# Prompt Chaining — Agentic Design Pattern #1

> Learn the **Prompt Chaining** agentic pattern through 4 hands-on examples.
> Runs locally on **Ollama** — no API key, no cloud, no cost.

---

## What is Prompt Chaining?

Instead of asking an LLM to do everything in one prompt, you break the task into focused steps. The output of each step becomes the input of the next.
```
Input → [Step 1] → output → [Step 2] → output → [Step 3] → Final Result
```

One prompt. One job. Each step is simpler, more accurate, and easier to debug.

---

## Patterns Covered

### 1 · Linear Chain
Each step's output feeds directly into the next.
```
raw text → [Extract facts] → [Summarise] → [Format as headline]
```

### 2 · Conditional Chain
Step 1 classifies the input. Python routes to a different prompt based on the result.
```
message → [Classify: complaint / question / praise] → [Specialist prompt]
```

### 3 · Validation Loop
Model generates, then self-validates. Retries with the failure reason fed back until it passes or hits max attempts.
```
task → [Generate] → [Validate] → PASS? return : retry with feedback
```

### 4 · Role-Based Pipeline
Same model, different system prompts = different personas at each step.
```
topic → [Writer] → [Critic] → [Editor] → polished output
```

---

## Quickstart

**1. Install Ollama**
```bash
# https://ollama.com/download
```

**2. Pull a model**
```bash
ollama pull qwen2.5
```

**3. Install dependencies**
```bash
pip install openai
```

**4. Run**
```bash
python prompt_chaining_ollama.py
```

---

## Configuration

Edit the top of the file to switch model or endpoint:
```python
MODEL    = "qwen2.5"                    # any model you have pulled
BASE_URL = "http://localhost:11434/v1"  # default Ollama endpoint
```

Other models to try:
```bash
ollama pull llama3.2   →  MODEL = "llama3.2"
ollama pull mistral    →  MODEL = "mistral"
ollama pull phi3       →  MODEL = "phi3"
```

---

## Project Structure
```
prompt_chaining_ollama.py   ← all 4 patterns in one file
README.md
```

One helper function powers everything:
```python
def ask(prompt: str, system: str = "You are a helpful assistant.") -> str:
    """Send a single prompt and return the model's reply as a string."""
```

That's the entire framework.

---

## Sample Output
```
███████████████████████████████████████████████████████
  PROMPT CHAINING — Ollama Learning Project
  Model: qwen2.5
███████████████████████████████████████████████████████

═══════════════════════════════════════════════════════
  Pattern 1 · Linear Chain
═══════════════════════════════════════════════════════
  Flow: Extract → Summarise → Format

  ── Step 1: Extract facts
  • JWST launched 25 December 2021 ...

  ── Step 2: Summarise
  The James Webb Space Telescope is humanity's ...

  ── Step 3: Format as headline
  Webb Telescope Reveals Universe in Stunning Infrared Detail
```

---

## Why This Matters

This pattern is the foundation of every serious AI agent. Once you understand how to chain prompts reliably, the rest of agentic design — parallelisation, tool use, memory — becomes much clearer.

---

## Part of a Series

| # | Pattern | Status |
|---|---------|--------|
| 1 | **Prompt Chaining** | ✅ This repo |
| 2 | Parallelisation | 🔜 Coming soon |
| 3 | Routing | 🔜 Coming soon |
| 4 | Orchestrator–Subagent | 🔜 Coming soon |
| 5 | Evaluator–Optimiser | 🔜 Coming soon |

---

## License

MIT
