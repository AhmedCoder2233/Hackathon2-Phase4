# Research: ChatKit UI Integration

**Feature Branch**: `003-chatkit-ui`  
**Created**: 2025-12-13  

## Resolution of NEEDS CLARIFICATION

### Clarification: Interpretation of "OpenAI ChatKit" in Constitution

**Context**: The project's constitution lists "OpenAI ChatKit" as a core frontend framework. The feature specification explicitly requires the use of the `@openai/chatkit-react` npm package.

**What we needed to know**: Does "OpenAI ChatKit" in the constitution refer specifically to the `@openai/chatkit-react` library or a broader framework that this library is a part of?

**Decision**: "OpenAI ChatKit" in the constitution refers to the integration using the `@openai/chatkit-react` library.

**Rationale**: The user's explicit instruction in the feature description to "ONLY use @openai/chatkit-react package as shown in example" clarifies that the library is the intended component for "OpenAI ChatKit" integration within this project's context. There are no indications of a broader framework beyond this specific library being intended or utilized.

**Alternatives considered**:
- Assuming "OpenAI ChatKit" implies a larger framework, potentially requiring additional setup or libraries. This was rejected as it contradicts the explicit instruction to use only the specified `npm` package.
