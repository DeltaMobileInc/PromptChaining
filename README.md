# Prompt Chaining — Agentic Design Pattern #1

Learn the Prompt Chaining pattern through 4 runnable examples.
Runs locally on **Qwen via Ollama** — no API key, no cost.

## What is Prompt Chaining?

Break a complex task into focused steps.
The output of each step becomes the input of the next.
```
Input → [Step 1] → output → [Step 2] → output → [Step 3] → Final
```

One prompt per job. Cleaner outputs. Easier to debug.

## Setup

**1. Install Ollama**
https://ollama.com/download

**2. Pull Qwen**
```bash
ollama pull qwen2.5
```

**3. Install dependencies**
```bash
pip install openai python-dotenv
```

**4. Run**
```bash
python prompt_chaining_simple.py          # all 4 examples
python prompt_chaining_simple.py 1        # just one
```

## The 4 Patterns

| # | Pattern | Concept |
|---|---------|---------|
| 1 | Linear Chain | A → B → C, each output feeds the next |
| 2 | Conditional Chain | LLM classifies, Python picks the path |
| 3 | Validation Loop | Validate in Python, LLM corrects only if needed |
| 4 | Role Pipeline | Different persona per step via system prompt |

## Switch to Anthropic (optional)

Change one line in the file:
```python
BACKEND = "anthropic"   # was "ollama"
```

Add your key to `.env`:
```
ANTHROPIC_API_KEY=sk-ant-...
```

## Project Structure
```
prompt_chaining_simple.py   ← all 4 patterns in one file
.env                        ← API key (only needed for Anthropic)
```

Two helper functions power everything:

- `ask(prompt, system)` — calls the model, returns text
- `to_json(text)` — extracts and parses JSON from any response
