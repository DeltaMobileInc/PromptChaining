# Prompt Chaining — Agentic Design Pattern #1
> 4 chaining patterns in one file. Runs locally on Ollama. No API key needed.

## Setup
```bash
# 1. Install Ollama
#    https://ollama.com/download

# 2. Pull a model
ollama pull qwen2.5

# 3. Install dependencies
pip install openai

# 4. Run
python prompt_chaining_ollama.py
```

## The 4 Patterns

### 1 · Linear Chain
Each step's output feeds directly into the next.
```
raw text → [Extract facts] → [Summarise] → [Format as headline]
```

### 2 · Conditional Chain
Step 1 output drives control flow, not content.
Python routes to a different prompt based on the classification.
```
message → [Classify: complaint / question / praise] → [Specialist prompt]
```

### 3 · Validation Loop
Model generates, then self-validates. Retries with the failure
reason fed back until it passes or hits max attempts (default: 3).
```
task → [Generate] → [Validate] → PASS? return : retry with feedback
```

### 4 · Role-Based Pipeline
Same model, different system prompts = different personas.
```
topic → [Writer] → [Critic] → [Editor] → polished output
```

## Configuration

Edit the top of the file to change model or endpoint:
```python
MODEL    = "qwen2.5"                    # any model you have pulled
BASE_URL = "http://localhost:11434/v1"  # default Ollama endpoint
```

Other models to try:
```bash
ollama pull llama3.2   # then set MODEL = "llama3.2"
ollama pull mistral    # then set MODEL = "mistral"
ollama pull phi3       # then set MODEL = "phi3"
```

## Core Helper

Everything runs through one function:
```python
def ask(prompt: str, system: str = "You are a helpful assistant.") -> str:
    """Send a single prompt and return the model's reply as a string."""
```

That's the entire framework.
