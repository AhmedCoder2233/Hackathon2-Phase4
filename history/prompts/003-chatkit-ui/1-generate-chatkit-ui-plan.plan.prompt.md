---
id: 1
title: Generate ChatKit UI Plan
stage: plan
date: 2025-12-13
surface: agent
model: gemini-model
feature: 003-chatkit-ui
branch: 003-chatkit-ui
user: Ahmed
command: /sp.plan
labels: ["planning", "chatkit-ui"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- specs/003-chatkit-ui/plan.md
- specs/003-chatkit-ui/research.md
- specs/003-chatkit-ui/data-model.md
- specs/003-chatkit-ui/quickstart.md
- GEMINI.md
tests:
-
---

## Prompt

```text
---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/powershell/setup-plan.ps1 -Json` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\'m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `.specify/memory/constitution.md`. Load IMPL_PLAN template (already copied).

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

4. **Stop and report**: Command ends after Phase 2 planning. Report branch, IMPL_PLAN path, and generated artifacts.

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Agent context update**:
   - Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType gemini`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage: 
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.
```

## Response snapshot

The implementation planning workflow has been executed. This involved:
- Running the `setup-plan.ps1` script to initialize the plan.md file and retrieve paths.
- Reading the feature specification (spec.md) and the project constitution.
- Filling out the `plan.md` with technical context, a detailed constitution check, and a project structure decision. All constitution gates passed, and no new clarifications were required.
- Creating `research.md` to document the resolution of any `NEEDS CLARIFICATION` markers (one was resolved regarding "OpenAI ChatKit").
- Creating `data-model.md` to define the 'User' entity, focusing on `user_id` generation.
- Creating `quickstart.md` to provide high-level setup and running instructions for the feature.
- Running `update-agent-context.ps1` to update the agent's knowledge base with the new technologies (`@openai/chatkit-react`, Next.js, React, TypeScript).

All required artifacts for Phase 0 and Phase 1 of the planning process have been generated.

## Outcome

- ✅ Impact: Plan for ChatKit UI Integration feature is complete and documented.
- 🧪 Tests: No tests were run in this planning phase.
- 📁 Files: `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, and `GEMINI.md` were created/updated.
- 🔁 Next prompts: Next step is to proceed with task breakdown (`/sp.tasks`).
- 🧠 Reflection: Encountered repeated issues with `run_shell_command` and PowerShell script execution due to pathing and quoting issues, necessitating a fallback to agent-native PHR creation.

## Evaluation notes (flywheel)

- Failure modes observed: `run_shell_command` with complex PowerShell commands and paths containing spaces.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): When executing PowerShell scripts, always use the absolute path and ensure proper quoting for arguments, especially those with spaces or special characters. If direct execution fails repeatedly, consider writing arguments to a temporary file and passing the file path.

```

Task: Analyze the potentially_problematic_string. If it's syntactically invalid due to incorrect escaping (e.g., "\n", "\t", "\\", "\'", '"'), correct the invalid syntax. The goal is to ensure the text will be a valid and correctly interpreted.

For example, if potentially_problematic_string is "bar\nbaz", the corrected_new_string_escaping should be "bar\nbaz".
If potentially_problematic_string is console.log(\"Hello World\"), it should be console.log("Hello World").

Return ONLY the corrected string in the specified JSON format with the key 'corrected_string_escaping'. If no escaping correction is needed, return the original potentially_problematic_string.
