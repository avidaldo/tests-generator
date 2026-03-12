# Advanced Prompting Techniques: Adversarial Filters and Structural Design


## 1. Adversarial Filters

The **Adversarial Filter** is a structural self-correction technique that forces the model to act as its own "critic" or "judge" during generation, using its reasoning capabilities to validate the quality of its own output before finalising it.

### Mechanism: "Induced Cognitive Dissonance"

Traditionally, an LLM acts as a linear probabilistic generator. If asked to "invent an error", it will do so by seeking superficial plausibility. The adversarial filter introduces **logical friction**:

1.  **Generation:** The model proposes an option (e.g. a distractor in an exam).
2.  **Forced Validation (The Filter):** The model is required to generate a **rigorous justification** (Feedback) for why that option is incorrect.

If the model has generated an ambiguous or partially correct option, it will "struggle" when trying to justify its absolute falseness.
*   *Symptom:* The model generates explanations with nuance ("well, it's almost true but...").
*   *Result:* Upon detecting this explanatory difficulty (internal incoherence), the model tends to discard the option and regenerate one that is unambiguously false and easy to refute, thus raising item quality.

**Practical Application:** In Moodle XML generation, do not ask only for the question — require that the `<feedback>` fields be filled in.
> *"Validation: If you find it hard to explain why an option is incorrect, that is a sign it is ambiguous → Discard it."*

## 2. Scenario Triangulation vs. Atomicity

Instead of asking for "questions about concepts" (which leads to dictionary-style definitions), request "scenario triangulation".

*   **Atomicity:** "What is X?" → Recall/Memorisation.
*   **Triangulation:** "What happens to X if we change Y given context Z?" → Deep comprehension.

This forces the model to simulate a mental "world" where variables interact, reducing hallucinations caused by simple word association.

## 3. Explicit Negative Constraints

It is more effective to define the solution space by what is **NOT** allowed, especially to avoid common statistical biases in LLMs:

*   **Length bias:** "The correct answer must NOT be systematically the longest".
*   **Structural bias:** "Avoid the pattern of 3 similar answers and 1 absurd one".
*   **Triviality bias:** "Avoid questions of the type 'Which is the best definition?'".

## 4. Strict Structural One-Shot (Templates)

For code-generation or strict-format tasks (XML, JSON), providing a **complete template** (`<resources>`) is superior to describing the grammar.
*   *Instruction:* "Use EXACTLY this schema."
*   *Effect:* Frees the model from "syntactic creativity", allowing it to dedicate all computation to "semantic creativity" (the question content).

## 5. Conceptual Distinction: Contrarian vs. Adversarial

Although both techniques use logical opposition, they differ fundamentally in their objective and the phase of the workflow where they are applied.

### Contrarian Prompting (External Debate)
This is an **exploration and review** technique. The model is asked to adopt a different "persona" to challenge the user or a given input.
*   **Mechanics:** "Adopt the role of X and criticise Y".
*   **Phase:** Ideation, Brainstorming, Draft Review.
*   **Objective:** Reduce the user's confirmation bias, find blind spots, or generate counter-arguments.
*   *Example:* "Criticise this code. Tell me which edge cases I am ignoring."

### Adversarial Filters (Internal Quality Control)
This is a **validation and intrinsic consistency** technique. The model is forced to perform an auxiliary task that is incompatible with poor execution of the main task.
*   **Mechanics:** "Generate X, and rigorously demonstrate why X satisfies condition Z. If you cannot demonstrate it, X is not valid."
*   **Phase:** Final output generation (Production).
*   **Objective:** Eliminate hallucinations, ambiguities, or low-quality responses *during* the inference process.
*   *Use Case (Exams):* The "logic trap". By requiring an explanation of a distractor's error, if the distractor is ambiguous the explanation will be weak, which alerts the model to discard it.

---

## 6. Reasoning Models and Chain-of-Thought (CoT)

With the arrival of reasoning models (o1-style, DeepSeek-R1), the rules around *Chain-of-Thought* have evolved.

### The Explicit CoT Paradox
In standard models (GPT-4, Claude 3.5), asking to "think step by step" (*Explicit CoT*) improves performance. In reasoning models, doing this can be **counterproductive** because it interferes with their internal reasoning tokens (*Internal CoT*), degrading quality or producing loops.

### The "Functional Output Constraint" Strategy
Instead of asking "show me how you think" (forbidden/inefficient), we ask **"give me a result that requires having thought deeply"**.

*   **Technique:** Require a complex output artefact that acts as proof of intellectual work.
*   **Application in the Moodle Test Skill:**
    *   We do NOT ask: *"Analyse the question before writing the XML"*.
    *   We ask: *"Fill in the mandatory `<feedback>` field explaining the error didactically."*

This forces the model to align its internal reasoning to produce that high-quality output. The `<feedback>` acts as a "reasoning anchor" in the final response, requiring the model's internal logic to be sound in order to write it — without needing to request the explicit process.
