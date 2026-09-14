# AI Banking Servicing Agent — Project Context

## Purpose

This file is the persistent project handoff and progress record for the `ai-banking-servicing-agent` project.

It should allow a new ChatGPT conversation, coding assistant, reviewer, or future contributor to understand:

- what the project is
- why it exists
- what has already been implemented
- what is currently being learned
- what architecture decisions have been made
- what is intentionally not implemented yet
- what branch/work is currently active
- what should happen next
- what claims are safe to make on a resume

Treat this file as the source of truth for project progress.

---

# 1. Project Overview

Project:

`AI-Assisted Banking Servicing Platform`

Repository/workspace:

```text
C:\Users\Sudhanshu\Documents\ai-banking-servicing-agent
```

Primary goals:

1. Learn production-oriented AI agent engineering.
2. Build a realistic synthetic banking servicing application.
3. Gain practical experience with:
   - Google ADK
   - agent tools
   - sessions/state
   - workflows
   - structured outputs
   - MCP
   - LangChain
   - FastAPI
   - testing
   - reliability
   - observability
   - backend architecture
4. Produce defensible technical evidence for AI/software-engineering interviews.
5. Avoid claiming any technology before it has actually been implemented.

All banking/customer information in this project is synthetic.

No real banking systems or customer data are used.

---

# 2. Learning Philosophy

This project is being built incrementally.

For each major capability:

```text
CONCEPT
→ WHY
→ WHERE IT FITS
→ SMALLEST EXAMPLE
→ IMPLEMENT
→ RUN
→ INSPECT
→ TEST
→ INTERVIEW EXPLANATION
```

Do not build the entire architecture at once.

The user should understand the architecture and code rather than blindly copy a finished implementation.

---

# 3. Target Architecture

Longer-term architecture:

```text
User
 │
 ▼
FastAPI
 │
 ▼
Banking Servicing Agent / Orchestrator
 │
 ├── Google ADK
 │
 ├── Session / State
 │
 ├── Tools
 │
 ├── Workflow orchestration
 │
 └── Guardrails
 │
 ▼
MCP Client
 │
 ▼
Banking MCP Server
 │
 ├── Customer capability
 │
 ├── KYC capability
 │
 ├── Policy capability
 │
 └── Servicing capability
 │
 ▼
Synthetic services / databases / policy data
```

LangChain should eventually have a legitimate separate responsibility rather than duplicating Google ADK orchestration.

Possible responsibility:

```text
Policy retrieval
+
RAG
+
structured policy analysis
```

---

# 4. Core Engineering Principle

Use the LLM for:

- natural-language interpretation
- reasoning
- deciding which approved capability to invoke
- coordination
- summarization

Use deterministic systems for:

- authoritative banking information
- validation
- state mutation
- business rules
- database access
- external actions
- authorization
- critical decisions

Principle:

```text
LLM = reasoning / language layer

Python / APIs / database / rules
= authoritative execution layer
```

The LLM should not become the system of record.

---

# 5. Current Git State

Main branch:

```text
main
```

Current development branch:

```text
feature/adk-session-state
```

Workflow:

```text
main
    ↓
feature branch
    ↓
implementation
    ↓
tests
    ↓
review
    ↓
commit
    ↓
push
    ↓
merge
```

Do not commit incomplete experiments merely to create activity.

Use meaningful commits representing working milestones.

---

# 6. Python Environment

Python:

```text
Python 3.12.10
```

Virtual environment:

```text
.venv
```

Activate with PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Testing:

```powershell
python -m pytest -v
```

Use `python -m pytest` rather than plain `pytest`.

---

# 7. Google ADK Model

Originally attempted model:

```text
gemini-2.5-flash
```

This produced an availability error for the current Gemini API account.

Current working model:

```text
gemini-3.6-flash
```

Do not change back to `gemini-2.5-flash` unless availability is explicitly reverified.

---

# 8. Current Project Structure

Approximate structure:

```text
ai-banking-servicing-agent/
│
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── session_demo.py
│   └── .adk/
│
├── tests/
│   └── test_kyc_tools.py
│
├── docs/
│
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

`.env` must never be committed.

---

# 9. Implemented ADK Level 1

## Agent

A Google ADK agent exists:

```text
banking_servicing_agent
```

The agent uses:

```text
gemini-3.6-flash
```

Its current responsibility is synthetic banking KYC servicing.

---

# 10. Implemented KYC Tool

Implemented deterministic tool:

```python
get_kyc_requirements(customer_type: str) -> dict
```

Supported types:

```text
individual
business
```

Example individual result:

```python
{
    "status": "success",
    "customer_type": "individual",
    "documents": [
        "government-issued photo ID",
        "proof of address",
        "tax identification document",
    ],
    "data_source": "synthetic_demo_policy",
}
```

Example business requirements:

```text
business registration document
tax identification document
registered business address proof
authorized representative identification
```

Unsupported types return:

```python
{
    "status": "unsupported_customer_type",
    ...
}
```

Inputs are normalized using:

```python
customer_type.strip().lower()
```

---

# 11. Grounding / Hallucination Lesson

An important problem was discovered during the first agent implementation.

The deterministic tool only returned:

```text
government-issued photo ID
```

but the model initially added examples such as passports or driver's licenses.

Those examples were not returned by the tool.

This demonstrated:

```text
trusted tool result
≠
automatically trusted final LLM answer
```

The agent instruction was strengthened so that responses grounded in tool output must use only facts explicitly returned by the tool.

Current principle:

```text
Tool result
→ trusted source

LLM final response
→ must remain constrained to tool evidence
```

The agent successfully refused to invent unsupported photo-ID examples afterward.

---

# 12. Existing Unit Tests

Current tests cover:

1. individual KYC requirements
2. business KYC requirements
3. unsupported customer type
4. normalization of input

Current known status:

```text
4 tests passing
```

Command:

```powershell
python -m pytest -v
```

There is currently an ADK deprecation warning originating from framework internals.

It is not currently blocking the project.

---

# 13. ADK Level 2 — Runner, Session, State

Current work focuses on:

```text
Runner
Session
SessionService
State
ToolContext
Events
state_delta
```

---

# 14. Runner

The project now executes the agent programmatically using:

```python
Runner
```

Conceptually:

```text
User input
   ↓
Runner
   ↓
Session
   ↓
Agent
   ↓
Model
   ↓
Tools
   ↓
Events / state changes
```

The Runner coordinates the execution lifecycle.

---

# 15. SessionService

Current implementation uses:

```python
InMemorySessionService
```

Important limitation:

```text
process alive
→ sessions exist

process restarted
→ in-memory sessions disappear
```

This is currently intentional for learning.

Durable persistence has not yet been implemented.

---

# 16. Session

A Session represents a single conversation thread.

Current identifiers include concepts such as:

```text
APP_NAME
USER_ID
SESSION_ID
```

The same session is reused across multiple conversational turns.

A session contains:

- event history
- structured state
- metadata/identity information

---

# 17. State

Initial demonstrations pre-seeded state:

```python
{
    "customer_type": "individual"
}
```

The agent instruction could access the value using ADK state injection:

```text
{customer_type?}
```

The `?` means the value is optional.

Without the optional form, a missing state value can cause an error.

---

# 18. Multi-Turn Session Demonstration

The project successfully executed multiple user turns through the same session.

Example:

```text
Turn 1:
What customer type is associated with this session?

Turn 2:
What KYC documents do I need?
```

The same session retained:

```python
{
    "customer_type": "individual"
}
```

The second turn successfully used that context.

---

# 19. Event History

The project now inspects:

```python
updated_session.events
```

A two-turn KYC interaction demonstrated events such as:

```text
User message
Model response

User message
Model function call
Tool function response
Final model response
```

This showed that an agent interaction is not simply:

```text
User → LLM → answer
```

Instead it can be:

```text
User
 ↓
LLM
 ↓
function call
 ↓
deterministic tool
 ↓
function response
 ↓
LLM
 ↓
final response
```

---

# 20. Conversation History vs State

Important distinction:

Conversation history:

```text
User said X
Agent said Y
Tool returned Z
```

State:

```python
{
    "customer_type": "business"
}
```

Conversation history is conversational context.

State is explicit structured application context.

Engineering principle:

If downstream application logic reliably depends on a value, prefer structured state rather than expecting the LLM to rediscover it from old conversation messages.

---

# 21. Dynamic State Mutation

The project now supports dynamically changing session state based on a user interaction.

Implemented tool:

```python
set_customer_type(
    customer_type: str,
    tool_context: ToolContext,
) -> dict
```

Supported values:

```text
individual
business
```

The tool validates the requested value before modifying state.

Core operation:

```python
tool_context.state["customer_type"] = normalized_type
```

---

# 22. ToolContext

`ToolContext` is injected by ADK into the tool execution.

The model chooses something logically equivalent to:

```text
set_customer_type(customer_type="business")
```

The LLM does not need to generate `ToolContext`.

The framework supplies it during execution.

---

# 23. Verified Dynamic State Flow

Successful interaction:

```text
Initial state:
{}
```

User:

```text
I'm a business customer.
```

The model called:

```text
set_customer_type(customer_type="business")
```

The deterministic Python tool executed.

ADK recorded:

```python
state_delta={
    "customer_type": "business"
}
```

The final session state became:

```python
{
    "customer_type": "business"
}
```

Then the user asked:

```text
What KYC documents do I need?
```

The agent used:

```text
customer_type = business
```

and called:

```text
get_kyc_requirements("business")
```

The final answer correctly returned business KYC requirements.

---

# 24. State Mutation Responsibility

Important interview-level distinction:

The LLM does not directly modify application state.

The flow is:

```text
LLM
 │
 │ decides that tool should be invoked
 ▼
set_customer_type()
 │
 │ validates input
 ▼
ToolContext
 │
 │ writes state
 ▼
ADK runtime
 │
 │ records state_delta
 ▼
SessionService
 │
 │ applies update
 ▼
Session
```

Strong explanation:

> Gemini determines that the `set_customer_type` tool should be invoked and supplies the customer type argument. The deterministic Python tool validates the value and writes it using ADK's ToolContext. ADK captures the modification as a state delta, and the SessionService applies it to the session.

---

# 25. Function Call vs Successful Action

Another important distinction discovered from event inspection.

Model function-call event:

```text
set_customer_type(customer_type="business")
```

had:

```python
state_delta={}
```

This represents the requested operation.

The following tool-response event contained:

```python
state_delta={
    "customer_type": "business"
}
```

This represents the successfully executed state mutation.

Principle:

```text
model requesting an action
≠
system successfully completing the action
```

This is especially important for future banking operations such as:

```text
create_service_request
update_address
freeze_account
submit_case
approve_action
```

---

# 26. Current ADK Skills Actually Implemented

Truthfully implemented:

- Google ADK Agent
- Gemini-backed ADK agent
- deterministic Python tools
- tool registration
- tool invocation
- grounded tool responses
- unsupported-input handling
- Runner
- InMemorySessionService
- Session
- multi-turn agent execution
- structured session state
- state injection in instructions
- dynamic state modification
- ToolContext
- event inspection
- function-call events
- function-response events
- state delta inspection
- deterministic state validation
- unit testing

---

# 27. Current Resume-Safe Claims

Safe claims include:

> Built a Python-based synthetic banking servicing agent using Google ADK and Gemini with deterministic tool invocation for KYC requirements.

> Implemented multi-turn ADK sessions and structured session state using Runner, InMemorySessionService, and ToolContext.

> Implemented controlled state mutation and validated agent execution through ADK event history and state deltas.

> Added grounding safeguards so model responses remain constrained to authoritative synthetic tool output.

> Added unit tests covering supported, unsupported, and normalized KYC tool inputs.

Do not describe this as a production banking system.

---

# 28. Technologies NOT Yet Implemented

Do not claim these as implemented yet:

- MCP
- LangChain
- FastAPI integration
- MongoDB
- Kafka
- persistent ADK session database
- production authentication
- production RBAC
- production deployment
- production observability stack
- production banking APIs
- production RAG
- vector database
- multi-agent system
- checkpointing
- streaming
- durable workflow engine

These may appear on the roadmap, but not as completed implementation.

---

# 29. Current ADK Learning Roadmap

## Level 1 — Agent + Tool

Status:

```text
COMPLETE
```

Implemented:

- ADK Agent
- Gemini
- deterministic KYC tool
- tool registration
- invocation
- grounding

---

## Level 2 — Runner + Session + State

Status:

```text
IN PROGRESS / MAJOR CORE CONCEPTS WORKING
```

Implemented:

- Runner
- Session
- InMemorySessionService
- multi-turn execution
- state
- state injection
- ToolContext
- dynamic state changes
- event inspection
- state_delta

Still to do:

- tests around session/state behavior
- cleaner separation of demo/debug code
- state scopes
- deeper persistence discussion
- possibly user/app/temp state scopes
- finalize Level 2 interview explanations

---

## Level 3 — Multiple Banking Tools

Planned examples:

```text
get_customer_profile()
get_kyc_status()
create_service_request()
get_case_status()
```

Goal:

Move from a one-capability demo toward real tool-selection and workflow reasoning.

---

## Level 4 — Structured Outputs

Planned:

- Pydantic schemas
- typed response contracts
- validation
- model output constraints
- structured failure responses

---

## Level 5 — Reliability

Planned:

- invalid arguments
- tool failures
- retries
- timeouts
- error boundaries
- safe fallback behavior
- idempotency discussion

---

## Level 6 — Callbacks / Guardrails / Observability

Planned:

- callbacks
- logging
- audit events
- tool invocation tracking
- latency monitoring
- model usage/cost awareness
- safety controls

---

## Level 7 — Multi-Agent

Only implement if a genuine architecture requirement emerges.

Do not add multiple agents purely for keyword coverage.

Potential future separation might include:

```text
servicing agent
policy agent
workflow agent
```

but this requires architectural justification first.

---

# 30. MCP Roadmap

MCP comes after sufficient ADK understanding.

Current:

```text
Gemini
 ↓
ADK
 ↓
Python tool
```

Future:

```text
Gemini
 ↓
ADK
 ↓
MCP client
 ↓
MCP server
 ↓
banking capability
```

Potential MCP tools:

```text
get_customer_profile
get_kyc_status
search_policy
create_service_request
get_case_status
```

Goal:

Understand what MCP adds instead of wrapping existing functions blindly.

---

# 31. LangChain Roadmap

LangChain should not simply duplicate the ADK agent.

Likely responsibility:

```text
policy retrieval
+
RAG
+
structured policy analysis
```

Before implementing LangChain, answer:

> What responsibility does LangChain have that ADK does not already handle in this application?

If that cannot be answered clearly, do not add LangChain yet.

---

# 32. FastAPI Roadmap

FastAPI will eventually expose agent capabilities through HTTP APIs.

Potential flow:

```text
Client
 ↓
FastAPI
 ↓
authentication / validation
 ↓
ADK agent/service
 ↓
tools / MCP
 ↓
structured response
```

FastAPI integration has not yet been implemented.

---

# 33. Data / Persistence Roadmap

Potential relational database:

```text
PostgreSQL
```

Potential document database:

```text
MongoDB
```

MongoDB should only be introduced if nested/document-oriented workflow state genuinely benefits from it.

Do not add a database merely to claim the technology.

---

# 34. Queue / Kafka Roadmap

Kafka is not currently implemented.

Potential future use cases:

```text
case-created event
manual-review request
customer-notification event
audit pipeline
long-running servicing workflow
```

Before Kafka, potentially demonstrate the architecture using a simpler queue.

Kafka should only be added if asynchronous/event-driven workflow needs justify it.

---

# 35. Production Engineering Topics To Eventually Cover

- configuration management
- secret management
- environment separation
- structured logging
- retries
- timeouts
- idempotency
- authentication
- authorization
- RBAC
- least privilege
- audit trails
- observability
- metrics
- tracing
- cost monitoring
- prompt injection
- hallucination controls
- human-in-the-loop
- malformed model output
- tool validation
- failure recovery
- sensitive-data handling
- Docker
- health endpoints
- deployment

---

# 36. Important Architecture Questions

The user should eventually be able to answer:

1. Why use an agent instead of a normal API?
2. When should deterministic logic be preferred over an LLM?
3. What is the difference between Agent, Runner, Session, SessionService, State, and ToolContext?
4. What does ADK store in event history?
5. What is a `state_delta`?
6. Why should tools modify state through ToolContext?
7. What is the difference between conversation history and structured state?
8. What is the difference between requesting a tool call and completing an action?
9. What happens if InMemorySessionService restarts?
10. Why must final model responses still be grounded even if tool results are trusted?
11. Where should authorization checks happen?
12. When is an agent unnecessary?
13. What does MCP add?
14. What responsibility should LangChain own?
15. How would this architecture change for real banking data?

---

# 37. Current Next Step

Current stopping point:

Dynamic session-state mutation through `ToolContext` works successfully.

The last verified run demonstrated:

```text
"I'm a business customer."
        ↓
set_customer_type("business")
        ↓
state_delta={"customer_type": "business"}
        ↓
session state persists
        ↓
"What KYC documents do I need?"
        ↓
get_kyc_requirements("business")
```

Next recommended work:

```text
1. Review Runner / Session / SessionService / State / ToolContext terminology.
2. Add tests for state-related behavior where practical.
3. Learn ADK state scopes:
   session state
   user: state
   app: state
   temp: state
4. Clean up session demo/debug output if necessary.
5. Finish ADK Level 2.
6. Commit and push feature/adk-session-state.
7. Begin Level 3 multi-tool banking capabilities.
```

---

# 38. Guidance for Future AI Assistants

When helping with this repository:

- Do not assume roadmap technologies are already implemented.
- Verify before making resume claims.
- Explain concepts before large architecture changes.
- Prefer incremental code changes.
- Give exact file paths.
- Give exact commands.
- Have the user run commands locally.
- Inspect actual output.
- Debug the failing layer instead of randomly changing unrelated code.
- Use current official documentation for version-sensitive ADK/MCP/LangChain APIs.
- Do not expose or request secrets.
- Never ask the user to paste their Gemini API key.
- Keep `.env` ignored.
- Keep banking data synthetic.
- Do not introduce multi-agent architecture without justification.
- Do not add MongoDB or Kafka merely for resume keywords.
- Prefer working, testable functionality over large unfinished architecture.

---

# 39. Update Policy

Update this file whenever one of the following occurs:

- new capability implemented
- architecture changes
- branch changes
- important bug discovered
- important design decision made
- tests added
- milestone completed
- dependency added
- model/provider changed
- resume evidence changes
- new known limitation discovered

After completing a milestone, update:

```text
Current Status
Implemented
Not Implemented
Known Limitations
Next Step
Resume-Safe Claims
```

This file should remain concise enough to read but detailed enough to reconstruct the project context in a completely new conversation.