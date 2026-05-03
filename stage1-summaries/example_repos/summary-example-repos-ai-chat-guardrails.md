<!-- markdownlint-disable MD024 MD025 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | README.md | `.md` | ✅ |
| 2 | pyproject.toml | `.toml` | ✅ |
| 3 | .env.local.example | `.env` | ✅ |
| 4 | .env.remote.example | `.env` | ✅ |
| 5 | prompts/system.txt | `.txt` | ✅ |
| 6 | prompts/judge.txt | `.txt` | ✅ |
| 7 | main.py | `.py` | ✅ |
| 8 | chatbot/config.py | `.py` | ✅ |
| 9 | chatbot/engine.py | `.py` | ✅ |
| 10 | chatbot/backends/factory.py | `.py` | ✅ |
| 11 | chatbot/backends/gemini.py | `.py` | ✅ |
| 12 | chatbot/backends/ollama.py | `.py` | ✅ |
| 13 | chatbot/guardrails/input_guard.py | `.py` | ✅ |
| 14 | chatbot/guardrails/output_guard.py | `.py` | ✅ |
| 15 | docs/test_cases.md | `.md` | ✅ |
| 16 | tests/test_engine.py | `.py` | ✅ |
| 17 | tests/test_input_guard.py | `.py` | ✅ |
| 18 | tests/test_output_guard.py | `.py` | ✅ |

# Content

## [Source: README.md]

The README frames the project as a didactic but production-shaped chatbot architecture: a Python conversational agent that can call either a local Ollama model or a remote Gemini model, with guardrails before and after the model call.

The core teaching pattern is explicit:

- validate the user message before spending tokens,
- send only accepted inputs to the LLM,
- validate the model response before showing it,
- keep the backend and guardrails decoupled.

The document also explains the intended project structure, the message flow, the environment variables, and why separate `.env.*.example` templates are standard practice.

Several architecture decisions are described as intentional simplifications:

- terminal CLI instead of web UI,
- no streaming because output validation needs the full response,
- single-session state instead of persistent multi-user storage.

The README closes with realistic extensions such as Gradio, FastAPI, persistent history, embedding-based guardrails, and PII detection.

## [Source: pyproject.toml]

The project metadata identifies the package as `guardrailed-chatbot`, requires Python `>=3.13`, and keeps the dependency set small and teaching-oriented.

Runtime dependencies are:

- `google-genai` for Gemini,
- `ollama` for local chat,
- `pydantic-settings` plus `python-dotenv` for configuration.

Development dependencies are just `pytest` and `pytest-mock`, which reinforces that testing is part of the intended learning surface.

## [Source: .env.local.example]

The local environment template documents the Ollama configuration surface:

- `CHAT_MODE=ollama`,
- a local model name such as `llama3.2`,
- `BASE_URL` for the Ollama server,
- `MAX_HISTORY_TURNS`,
- `MAX_INPUT_CHARS`.

This file makes the local mode concrete and reproducible, and it explicitly reminds the user to pull the model before running the app.

## [Source: .env.remote.example]

The remote environment template documents the Gemini configuration surface:

- `CHAT_MODE=gemini`,
- a Gemini model name,
- `API_KEY`,
- the same history and input-length controls.

Together with the local template, this shows that the project keeps behavioral settings shared while switching only the provider-specific fields.

## [Source: prompts/system.txt]

The system prompt is deliberately minimal: the assistant should be helpful, concise, and technical. The point is not persona design but providing a stable baseline instruction that the backend always receives.

## [Source: prompts/judge.txt]

The judge prompt is even more minimal: the model should behave as a strict security evaluator. This is the prompt used for the secondary LLM-as-a-judge path in both guardrails.

## [Source: main.py]

`main.py` is intentionally narrow in scope. Its own top comment defines its job as:

- load configuration,
- instantiate `ChatEngine`,
- verify connectivity,
- run the terminal loop.

Operationally, it:

- prints friendly configuration and connection errors,
- checks the backend connection before starting the conversation,
- handles `KeyboardInterrupt` and `EOFError` cleanly,
- treats `exit`, `quit`, and `bye` as explicit termination commands,
- skips empty inputs instead of sending them into the pipeline.

This file is therefore a thin shell around the engine rather than a place where application logic accumulates.

## [Source: chatbot/config.py]

The configuration layer uses `pydantic-settings` with `.env` loading and ignores unknown environment variables. It also loads the system and judge prompts directly from files, which keeps prompt text outside the Python modules that consume it.

The file defines:

- `BaseChatConfig` for shared fields,
- `GeminiConfig` for remote-only settings,
- `OllamaConfig` for local-only settings.

The important behavioral detail is in `load_config()`: it first reads a base configuration, then returns `GeminiConfig` only when the normalized mode is exactly `gemini`; otherwise it falls back to `OllamaConfig`. That means the effective mode names in code are `gemini` and `ollama`, even though the README often explains them conceptually as remote versus local.

## [Source: chatbot/engine.py]

`ChatEngine` is the orchestrator. It owns:

- the conversation history,
- the main backend,
- a separate judge backend,
- the full per-turn control flow.

The method `chat()` implements a five-step pipeline:

1. input guardrail,
2. append user message,
3. backend call,
4. output guardrail,
5. append assistant response.

Two details matter conceptually.

First, the engine never raises exceptions outward from `chat()`. Instead, backend failures become user-facing error strings, which keeps the CLI loop simple.

Second, if the backend fails or the output guard blocks the response, the engine removes the just-added user message from history so the next turn starts cleanly.

The file also includes a nested `llm_judge()` helper that reuses the judge backend with a one-message history, and a `_trim_history()` method that keeps only the most recent turns based on `max_history_turns`.

## [Source: chatbot/backends/factory.py]

The factory module establishes a small backend abstraction. `BackendProtocol` requires three things:

- an `assistant_role`,
- `get_response(history)`,
- `ping()`.

The project uses two factory functions:

- `create_backend(config)` for normal generation with the main system prompt,
- `create_judge_backend(config)` for safety evaluation with the judge prompt.

Both rely on the same private `_build_backend()` helper, which means the judge path and the normal response path differ only in prompt, not in provider implementation.

The backend imports are lazy, so provider-specific modules are only imported when the chosen mode requires them.

## [Source: chatbot/backends/gemini.py]

The Gemini backend wraps the `google-genai` client. It identifies assistant messages with role `model`, checks connectivity by fetching model metadata, and converts the internal history format into Gemini `Content` and `Part` objects.

Its generation settings are fixed in code:

- the configured system instruction,
- `max_output_tokens=1024`,
- `temperature=0.7`.

So the backend is deliberately simple and opinionated rather than highly configurable.

## [Source: chatbot/backends/ollama.py]

The Ollama backend uses the official Python client, identifies assistant messages with role `assistant`, and checks availability through `ollama.list()`.

Unlike the Gemini backend, it prepends the system prompt as a normal `system` message before replaying the rest of the conversation history. The result returned to the engine is `response.message.content`.

This file preserves the key implementation difference between providers: Gemini receives a dedicated system instruction field, while Ollama receives the prompt inside the messages list.

## [Source: chatbot/guardrails/input_guard.py]

The input guardrail is structured as a fail-fast sequence of small checks.

The checks are:

1. non-empty and within `MAX_INPUT_CHARS`,
2. no blocked literal fragments such as `<script>` or SQL-like strings,
3. no regex-matched prompt injection phrases,
4. optional LLM-as-a-judge evaluation.

The file is unusually explicit about the limitations of regex-based security. It warns that heuristic detection is brittle, that attackers can rephrase prompt injections, and that the regex patterns are capped in length to avoid catastrophic backtracking.

The LLM judge path uses a structured prompt that asks for exactly `SAFE` or `UNSAFE: ...`, then turns any unsafe result into a user-facing rejection reason.

## [Source: chatbot/guardrails/output_guard.py]

The output guardrail mirrors the input guard in architecture but not in return contract. It checks:

1. the response is not effectively empty,
2. the response does not include known sensitive phrases,
3. an optional LLM judge does not detect a leak.

If validation passes, the function returns the cleaned response text itself rather than an empty string. The module comment calls out this asymmetry as intentional: the engine can receive the final stripped text in one call.

The file also treats the output guard as the last line of defense against prompt leakage, malformed responses, and policy-violating content.

## [Source: docs/test_cases.md]

The test-case document maps the conceptual testing strategy to three surfaces:

- input guardrail,
- output guardrail,
- engine orchestrator.

It states exactly what the automated tests are meant to demonstrate: input rejection, leak prevention, LLM-judge behavior, graceful backend failure handling, and history trimming.

This document is useful because it turns the tests from isolated assertions into an explicit specification of expected behavior.

## [Source: tests/test_input_guard.py]

The input-guard tests use safe and unsafe dummy judge functions to separate heuristic behavior from LLM-judge behavior.

They verify:

- empty and too-long messages are rejected,
- blocked fragments such as `<script>` and `DROP TABLE` are rejected,
- common prompt-injection phrasing is rejected,
- messages that pass heuristics can still be blocked by the LLM judge,
- the guard still works without a judge by running heuristics alone.

## [Source: tests/test_output_guard.py]

The output-guard tests verify the parallel behavior on the response side:

- whitespace-only and very short outputs are rejected,
- explicit sensitive strings such as `api_key` are blocked,
- the LLM judge can reject nuanced responses,
- approved outputs are stripped of surrounding whitespace.

These tests make the intended contract of `output_guard.validate()` very clear.

## [Source: tests/test_engine.py]

The engine tests patch backend creation so the orchestrator can be tested without real LLM providers.

The covered behaviors are:

- a successful turn appends both user and assistant messages,
- a backend failure returns a friendly error and leaves history empty,
- history trimming keeps the session bounded.

One subtle detail emerges from the trimming test: with `max_history_turns=2`, the asserted history length after three interactions is `5`, not `4`. That reflects the current implementation order in `ChatEngine`: trimming happens after the user message is appended but before the assistant response is added, so the final list can temporarily exceed the nominal `2 turns = 4 messages` bound by one assistant message.

# Cross-References

## Architecture and flow

- The README's message-flow diagram is implemented concretely by the separation among `main.py`, `chatbot/engine.py`, the backend factory, and the two guardrail modules. [Source: README.md; Source: main.py; Source: chatbot/engine.py; Source: chatbot/backends/factory.py; Source: chatbot/guardrails/input_guard.py; Source: chatbot/guardrails/output_guard.py]
- The project's single-responsibility story is real in code: `main.py` owns the CLI loop, `config.py` owns environment and prompt loading, `engine.py` owns orchestration, and the backend modules are provider-specific adapters. [Source: README.md; Source: main.py; Source: chatbot/config.py; Source: chatbot/engine.py; Source: chatbot/backends/gemini.py; Source: chatbot/backends/ollama.py]
- The judge path is not a separate system architecture; it reuses the same backend abstraction with a different prompt via `create_judge_backend()`. [Source: prompts/judge.txt; Source: chatbot/backends/factory.py; Source: chatbot/engine.py]

## Configuration and mode selection

- The environment templates and `config.py` together define the real provider switch: `gemini` selects `GeminiConfig`, while any other mode falls through to `OllamaConfig`. [Source: .env.local.example; Source: .env.remote.example; Source: chatbot/config.py]
- Prompt text lives in files and is loaded dynamically into configuration, so changing model instructions does not require editing the engine or backend logic. [Source: prompts/system.txt; Source: prompts/judge.txt; Source: chatbot/config.py]
- Both backends share the same conversation-history interface even though Gemini uses a system-instruction field and Ollama uses a `system` message in the chat payload. [Source: chatbot/backends/factory.py; Source: chatbot/backends/gemini.py; Source: chatbot/backends/ollama.py]

## Guardrails and evaluation strategy

- The input and output guards follow the same layered policy: cheap deterministic heuristics first, then optional LLM-as-a-judge evaluation for cases the heuristics may miss. [Source: chatbot/guardrails/input_guard.py; Source: chatbot/guardrails/output_guard.py]
- The README's explanation that input validation saves tokens is directly matched by the engine's order of operations: the input guard runs before the user message is appended and before the backend call. [Source: README.md; Source: chatbot/engine.py; Source: chatbot/guardrails/input_guard.py]
- The output guard is the reason the example avoids streaming: the architecture assumes the full model response is available before validation and display. [Source: README.md; Source: chatbot/guardrails/output_guard.py]

## Tests as executable specification

- `docs/test_cases.md` serves as a prose contract for the three automated test modules, and each test file matches the scenarios it documents. [Source: docs/test_cases.md; Source: tests/test_input_guard.py; Source: tests/test_output_guard.py; Source: tests/test_engine.py]
- The engine test suite reveals the effective history semantics more precisely than the engine docstring alone, especially around trimming behavior after a completed assistant turn. [Source: chatbot/engine.py; Source: tests/test_engine.py]

## Decision criteria and trade-offs

- Choose `ollama` when local execution, no API key, and offline teaching value matter more than model quality or hosted convenience; choose `gemini` when remote API access is acceptable. [Source: README.md; Source: .env.local.example; Source: .env.remote.example]
- Use the heuristic checks for fast rejection of obvious bad inputs and outputs, but rely on the judge path for nuanced jailbreaks or leaks that simple patterns will miss. [Source: chatbot/guardrails/input_guard.py; Source: chatbot/guardrails/output_guard.py; Source: README.md]
- Keep the CLI design when the learning goal is architecture and control flow; move to Gradio or FastAPI only when UI or deployment becomes part of the lesson. [Source: README.md; Source: main.py]
