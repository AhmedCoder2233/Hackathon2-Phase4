# Research: Add Dockerfile for Backend

## 1. Testing Framework Selection

- **Decision**: `pytest` will be the designated testing framework for the backend.
- **Rationale**: The project currently lacks a testing setup. `pytest` is the de-facto standard for testing in the Python ecosystem and has excellent integration with FastAPI. Adopting it now establishes a solid foundation for future quality assurance.
- **Alternatives Considered**: 
  - Python's built-in `unittest` framework was considered.
  - `pytest` was chosen for its simpler, more expressive syntax, powerful fixture model, and extensive plugin ecosystem.
