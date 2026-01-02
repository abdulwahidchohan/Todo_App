# AI Agent Instructions for Spec-Driven Development

## Core Mandate
As an AI architect implementing Spec-Driven Development (SDD), you must adhere to the following workflow:
1. **Specify** (Requirements in `specs/`)
2. **Plan** (Architecture in `specs/`)
3. **Tasks** (Breakdown in `specs/`)
4. **Implement** (Code in `/frontend` or `/backend`)

## Strict Enforcement Rules

### NO "Vibe Coding"
- **Never** write code without a corresponding specification in the `specs/` directory
- **Never** implement features based on assumptions or preferences
- **Never** add functionality that doesn't trace back to a documented requirement
- **Never** refactor or modify code without a clear requirement justification

### Requirement Traceability
- Every line of code must be traceable to a specific requirement in `specs/features/`
- Before implementing ANY code, verify the existence of a corresponding specification
- If a requirement is unclear, return to the specification phase for clarification
- Maintain clear links between code commits and specification documents

### Specification First Policy
- All requirements must be documented in `specs/features/` before any implementation
- Architecture decisions must be captured in `specs/plans/` before coding
- Task breakdowns must be detailed in `specs/tasks/` before development begins
- No exceptions to this policy are permitted

### Quality Assurance
- Verify that each implementation directly addresses the specified requirement
- Ensure code changes are minimal and targeted to the specific requirement
- Test implementations against the original specification criteria
- Reject any implementation that doesn't have a clear specification reference

## Enforcement Mechanism
Before writing any code, ask yourself:
1. Does a specification exist for this requirement in `specs/`?
2. Is the specification clear and unambiguous?
3. Can I trace this code change directly back to a requirement?
4. Would this change be possible without the corresponding specification?

If the answer to any of these questions is "no", return to the specification phase.

## Violation Consequences
Violating these rules results in:
- Invalidated implementation requiring restart from specification phase
- Potential architectural inconsistencies
- Loss of requirement traceability
- Compromised project integrity

## Exception Process
The only acceptable exception is for:
- Critical security patches that cannot wait for specification
- Emergency fixes for production-breaking bugs
- Even these must be documented and specifications created retroactively

All other implementations must follow the SDD workflow without exception.