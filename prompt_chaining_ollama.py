"""
Prompt Chaining with Ollama — Learning Project
================================================
Demonstrates 4 chaining patterns using a local Ollama model.
Each pattern is self-contained and clearly labelled.

Requirements:
    pip install openai python-dotenv
    ollama pull qwen2.5   (or any model you have locally)

Usage:
    python prompt_chaining_ollama.py
"""

from openai import OpenAI
import json

# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────

MODEL  = "qwen2.5"          # change to any model you have in Ollama
BASE_URL = "http://localhost:11434/v1"

client = OpenAI(
    base_url=BASE_URL,
    api_key="ollama",       # Ollama ignores the key; required by the OpenAI client
)


# ──────────────────────────────────────────────
# Core helper
# ──────────────────────────────────────────────

def ask(prompt: str, system: str = "You are a helpful assistant.") -> str:
    """Send a single prompt and return the model's reply as a string."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system",  "content": system},
            {"role": "user",    "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()


def separator(title: str):
    print("\n" + "═" * 55)
    print(f"  {title}")
    print("═" * 55)


def step(n: int, label: str, result: str):
    print(f"\n  ── Step {n}: {label}")
    print(f"  {result[:300]}{'...' if len(result) > 300 else ''}")


# ══════════════════════════════════════════════
# Pattern 1 — Linear Chain
# ══════════════════════════════════════════════
#
#   raw_text → [Extract] → [Summarise] → [Format]
#
# Each step's output feeds directly into the next.

def linear_chain(raw_text: str) -> str:
    separator("Pattern 1 · Linear Chain")
    print("  Flow: Extract → Summarise → Format\n")

    # Step 1: extract key facts
    facts = ask(
        f"Extract the 3–5 most important facts from this text. "
        f"List them as plain bullet points.\n\n{raw_text}"
    )
    step(1, "Extract facts", facts)

    # Step 2: summarise the extracted facts
    summary = ask(
        f"Summarise these bullet points in 2 sentences:\n\n{facts}"
    )
    step(2, "Summarise", summary)

    # Step 3: format as a polished one-liner
    result = ask(
        f"Rewrite this as a single, punchy headline (max 15 words):\n\n{summary}"
    )
    step(3, "Format as headline", result)

    return result


# ══════════════════════════════════════════════
# Pattern 2 — Conditional Chain
# ══════════════════════════════════════════════
#
#   input → [Classify] → (complaint | question | praise) → [Respond]
#
# Step 1 output is used as *control flow*, not content.

def conditional_chain(user_message: str) -> str:
    separator("Pattern 2 · Conditional Chain")
    print("  Flow: Classify → branch to specialist prompt\n")

    # Step 1: classify
    category = ask(
        f"Classify the following message into exactly one word: "
        f"complaint, question, or praise.\n\nMessage: {user_message}\n\nCategory:"
    ).lower().strip().split()[0]  # take first word in case model adds punctuation

    step(1, f"Classify → '{category}'", category)

    # Step 2: route to the right specialist prompt
    handlers = {
        "complaint": (
            "You are a warm, empathetic customer-support agent.",
            "Acknowledge the issue and offer a concrete next step:"
        ),
        "question": (
            "You are a knowledgeable, concise assistant.",
            "Answer clearly in 2–3 sentences:"
        ),
        "praise": (
            "You are a friendly brand ambassador.",
            "Thank the customer warmly and invite them to share their experience:"
        ),
    }

    system, instruction = handlers.get(
        category,
        ("You are a helpful assistant.", "Respond helpfully:")
    )

    response = ask(f"{instruction}\n\n{user_message}", system=system)
    step(2, f"Handle as '{category}'", response)

    return response


# ══════════════════════════════════════════════
# Pattern 3 — Validation Loop
# ══════════════════════════════════════════════
#
#   task → [Generate] → [Validate] → PASS? return : retry
#
# The model self-corrects until output meets criteria or
# max attempts are reached.

def validation_loop(task: str, max_attempts: int = 3) -> str:
    separator("Pattern 3 · Validation Loop")
    print(f"  Flow: Generate → Validate → retry up to {max_attempts}×\n")

    current_task = task

    for attempt in range(1, max_attempts + 1):
        print(f"\n  ── Attempt {attempt}/{max_attempts}")

        # Generate
        output = ask(f"Complete this task carefully:\n\n{current_task}")
        print(f"  Generated: {output[:200]}{'...' if len(output) > 200 else ''}")

        # Validate
        verdict_raw = ask(
            f"Task: {task}\n\n"
            f"Output to evaluate:\n{output}\n\n"
            f"Does the output fully and correctly satisfy the task? "
            f"Reply with exactly 'PASS' or 'FAIL: <one-sentence reason>'."
        )
        verdict = verdict_raw.strip()
        print(f"  Verdict:   {verdict}")

        if verdict.upper().startswith("PASS"):
            print(f"\n  ✓ Passed on attempt {attempt}")
            return output

        # Feed the failure reason back for the next attempt
        current_task = (
            f"{task}\n\n"
            f"Previous attempt was rejected for this reason: {verdict}\n"
            f"Fix that specific issue and try again."
        )

    print(f"\n  ⚠ Returning best effort after {max_attempts} attempts")
    return output


# ══════════════════════════════════════════════
# Pattern 4 — Role-Based Pipeline
# ══════════════════════════════════════════════
#
#   topic → [Writer] → [Critic] → [Editor] → polished output
#
# Same model, different system prompts = different "personas".

def role_pipeline(topic: str) -> str:
    separator("Pattern 4 · Role-Based Pipeline")
    print("  Flow: Writer → Critic → Editor\n")

    # Role 1: Writer drafts
    draft = ask(
        f"Write a short, engaging paragraph (4–6 sentences) about: {topic}",
        system="You are a creative writer with a clear, vivid style."
    )
    step(1, "Writer — draft", draft)

    # Role 2: Critic finds weaknesses
    critique = ask(
        f"Read this paragraph and list 2–3 specific improvements "
        f"(clarity, structure, missing detail):\n\n{draft}",
        system="You are a sharp, constructive editor. Be specific, not vague."
    )
    step(2, "Critic — feedback", critique)

    # Role 3: Editor applies feedback
    polished = ask(
        f"Revise the paragraph using the feedback below. "
        f"Keep it concise (4–6 sentences).\n\n"
        f"Original:\n{draft}\n\nFeedback:\n{critique}",
        system="You are a senior copy editor. Improve without over-rewriting."
    )
    step(3, "Editor — polished", polished)

    return polished


# ──────────────────────────────────────────────
# Run all four patterns
# ──────────────────────────────────────────────

if __name__ == "__main__":

    print("\n" + "█" * 55)
    print("  PROMPT CHAINING — Ollama Learning Project")
    print("  Model:", MODEL)
    print("█" * 55)

    # ── Pattern 1: Linear Chain ──────────────────
    sample_text = (
        "The James Webb Space Telescope (JWST) launched on 25 December 2021. "
        "It is the most powerful space telescope ever built, designed to observe "
        "the universe in infrared light. JWST can peer through dust clouds to see "
        "star-forming regions and study the atmospheres of exoplanets. Its primary "
        "mirror spans 6.5 metres, far larger than Hubble's 2.4-metre mirror. "
        "The telescope orbits around the L2 Lagrange point, 1.5 million km from Earth."
    )
    linear_chain(sample_text)

    # ── Pattern 2: Conditional Chain ─────────────
    messages = [
        "My order arrived broken and no one is responding to my emails!",
        "What is the difference between RAM and storage?",
        "I just wanted to say your product changed my life — thank you!",
    ]
    for msg in messages:
        print(f"\n  Input: \"{msg}\"")
        conditional_chain(msg)

    # ── Pattern 3: Validation Loop ────────────────
    validation_loop(
        "Write exactly 3 bullet points about the benefits of regular exercise. "
        "Each bullet must start with a verb."
    )

    # ── Pattern 4: Role Pipeline ──────────────────
    role_pipeline("how ocean currents regulate Earth's climate")

    print("\n\n" + "█" * 55)
    print("  All patterns complete.")
    print("█" * 55 + "\n")
    