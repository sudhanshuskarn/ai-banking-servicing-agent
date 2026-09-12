# AI-Assisted Banking Servicing Platform

A production-oriented AI engineering project exploring how **agentic AI, deterministic services, APIs, retrieval, workflow orchestration, and enterprise safeguards** can work together in a banking-servicing environment.

The project is being built incrementally, beginning with a **Google Agent Development Kit (ADK)** agent backed by deterministic synthetic banking tools and progressively evolving toward a modular architecture using **FastAPI, MCP, LangChain, retrieval/vector search, persistent data stores, asynchronous workflows, testing, observability, and containerization**.

> **Important:** This is an educational and portfolio project. All customer records, KYC information, policies, workflows, and banking data are synthetic. The application does not connect to or represent any real bank or production banking system.

---

## Project Goals

Banking servicing involves many structured systems and workflows:

- Customer profiles
- KYC requirements and status
- Account onboarding
- Policy and procedure lookup
- Case management
- Service requests
- Compliance workflows
- Human review and escalation

Traditional software is excellent when the user already knows the exact operation to perform.

For example:

```text
GET /customers/{id}/kyc-status
```

However, users often express goals in natural language:

```text
"Why is this customer's onboarding blocked,
what requirements are missing,
and what should happen next?"
```

There may be no single API corresponding to that request.

The goal of this project is to explore an architecture in which an AI agent can:

1. Understand a natural-language request.
2. Determine what information or actions are required.
3. Select approved tools and services.
4. Execute deterministic operations through controlled interfaces.
5. Retrieve relevant policy information when required.
6. Reason over verified results.
7. Produce a grounded structured response.
8. Escalate to deterministic workflows or human review where appropriate.

The AI agent is therefore **not the banking system itself**.

It acts as an intelligent coordination layer over controlled, authoritative capabilities.

---

# Current Status

## Implemented

The current milestone includes:

- Python 3.12 project
- Google Agent Development Kit (ADK)
- Gemini 3.6 Flash-backed ADK agent
- Deterministic synthetic KYC requirements tool
- ADK tool registration and invocation
- Natural-language request → agent → tool → response flow
- Tool-grounded response instructions
- Unsupported customer-type handling
- Protection against unsupported factual embellishment
- Unit tests for deterministic banking logic
- Pytest test suite
- Synthetic banking data only

Current tests:

```text
4 passed
```

Supported synthetic customer types:

```text
individual
business
```

---

## In Progress / Planned

The following capabilities are part of the engineering roadmap and should **not be interpreted as currently implemented**:

- ADK Runner, Sessions, and State
- Additional banking tools
- Structured agent outputs
- Pydantic validation
- Agent callbacks and guardrails
- Multi-step agent workflows
- Model Context Protocol (MCP)
- LangChain
- FastAPI service layer
- Policy retrieval / RAG
- Embeddings
- Vector database / vector search
- Persistent operational storage
- MongoDB where justified
- PostgreSQL where relational storage is appropriate
- Asynchronous task processing
- Kafka or another event/queue mechanism where justified
- Authentication and authorization
- Human-in-the-loop workflows
- Audit logging
- Observability
- Docker
- Integration testing
- Agent evaluations
- Deployment architecture

---

# Architecture

The target architecture is intentionally layered.

```text
                         ┌──────────────────────┐
                         │        User          │
                         │ Analyst / Employee   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │     API Boundary     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                  ┌─────────────────────────────────┐
                  │      Agent / Orchestration      │
                  │                                 │
                  │          Google ADK             │
                  │                                 │
                  │ Intent Understanding            │
                  │ Tool Selection                  │
                  │ Multi-step Reasoning            │
                  │ Session / State                 │
                  │ Guardrails                      │
                  └───────────────┬─────────────────┘
                                  │
                 ┌────────────────┼────────────────┐
                 │                │                │
                 ▼                ▼                ▼
        ┌────────────────┐ ┌──────────────┐ ┌─────────────────┐
        │ MCP Client     │ │  LangChain   │ │ Workflow Layer  │
        │                │ │              │ │                 │
        │ Tool access    │ │ Retrieval /  │ │ Deterministic   │
        │ boundary       │ │ Policy AI    │ │ workflow logic  │
        └───────┬────────┘ └──────┬───────┘ └────────┬────────┘
                │                 │                  │
                ▼                 ▼                  ▼
        ┌────────────────┐ ┌──────────────┐ ┌─────────────────┐
        │   MCP Server   │ │ Vector Store │ │ Queue / Events  │
        │                │ │              │ │                 │
        │ Banking tools  │ │ Embeddings   │ │ Kafka / similar │
        └───────┬────────┘ └──────────────┘ └─────────────────┘
                │
      ┌─────────┼──────────┬───────────────┐
      │         │          │               │
      ▼         ▼          ▼               ▼
 Customer    KYC Data    Cases          Policies
 Service     Service     Service        Service
      │         │          │               │
      └─────────┴──────────┴───────────────┘
                         │
                         ▼
               ┌────────────────────┐
               │ Persistent Storage │
               │                    │
               │ PostgreSQL /       │
               │ MongoDB where      │
               │ appropriate        │
               └────────────────────┘
```

This is the **target architecture**. The project is being implemented incrementally rather than creating every component at once.

---

# Core Engineering Principle

A central design principle of this project is:

> **Use the LLM for language understanding, reasoning, and flexible orchestration. Use deterministic software for authoritative facts, business rules, calculations, validation, and critical operations whenever possible.**

For example:

```text
User:
"What KYC documents do I need as an individual customer?"

              ↓

Gemini / ADK Agent
understands the natural-language request

              ↓

get_kyc_requirements(
    customer_type="individual"
)

              ↓

Deterministic Python logic

              ↓

Authoritative synthetic result

              ↓

Agent produces grounded response
```

The deterministic function itself does not require an LLM.

The model is used around the deterministic capability where natural-language interpretation or reasoning is useful.

---

# Why Use an Agent?

Not every API needs an AI agent.

A deterministic request such as:

```text
GET /kyc/requirements?customer_type=individual
```

can and should be handled directly when the caller already knows the exact operation.

Agents become more useful for requests such as:

```text
"Why is this customer's onboarding blocked?
What are they missing?
Which policy applies?
What should happen next?"
```

The agent may need to determine that it should:

```text
get_customer_profile()
        ↓
get_kyc_status()
        ↓
search_policy()
        ↓
determine appropriate next step
        ↓
optionally create_service_request()
        ↓
produce grounded response
```

The agent therefore provides flexible reasoning and orchestration over deterministic capabilities rather than replacing those capabilities.

---

# Google ADK

Google Agent Development Kit is the primary agent framework used for the orchestration layer.

The project is progressively exploring:

- Agents
- Agent instructions
- Tools
- Tool schemas
- Tool invocation
- Runner
- Sessions
- State
- Structured outputs
- Callbacks
- Guardrails
- Error handling
- Multi-step execution
- Multi-agent architecture only where justified
- Agent evaluation

## Current ADK Agent

The initial agent is:

```text
banking_servicing_agent
```

Its current responsibility is answering synthetic KYC requirement questions using an approved deterministic tool.

Current flow:

```text
User
 ↓
ADK Agent
 ↓
Gemini 3.6 Flash
 ↓
Tool selection
 ↓
get_kyc_requirements()
 ↓
Synthetic deterministic policy data
 ↓
Grounded agent response
```

---

# Deterministic Banking Tools

Tools represent controlled capabilities available to the agent.

Current tool:

```python
get_kyc_requirements(customer_type: str)
```

It provides synthetic KYC requirements for:

```text
individual
business
```

The function:

- normalizes customer type
- validates supported customer types
- retrieves deterministic requirements
- returns structured data
- identifies the synthetic data source
- returns an explicit unsupported status for unknown customer types

Planned tools include:

```text
get_customer_profile()
get_kyc_status()
get_kyc_requirements()
get_onboarding_status()
search_policy()
create_service_request()
get_service_request()
get_case_status()
```

These will remain deterministic wherever the underlying operation does not require generative reasoning.

---

# Grounding and Hallucination Control

An important reliability issue was identified during the first ADK implementation.

The deterministic KYC tool returned:

```text
government-issued photo ID
proof of address
tax identification document
```

The model initially added examples such as specific identity documents that were **not returned by the authoritative tool**.

This demonstrated an important agent-engineering principle:

> A trusted tool does not automatically guarantee a trusted final answer.

The agent instructions were strengthened so that responses based on authoritative banking tools must use only facts explicitly returned by those tools.

The updated behavior was tested with three scenarios.

### Supported request

```text
What KYC documents are required for an individual customer?
```

The agent returns only the tool-supported requirements.

### Missing knowledge

```text
Give me examples of acceptable government-issued photo IDs.
```

Because the synthetic policy tool does not contain examples, the agent states that the available information does not specify them rather than inventing examples.

### Unsupported customer type

```text
What KYC documents are required for a nonprofit customer?
```

The agent reports that the current synthetic system supports only:

```text
individual
business
```

This behavior will later be strengthened with structured outputs, validation, provenance, agent evaluations, and additional guardrails.

---

# Model Context Protocol (MCP)

MCP is planned as the standardized capability boundary between the agent and banking services.

Instead of permanently coupling the ADK agent directly to Python functions:

```text
ADK
 ↓
Python function
```

the architecture will evolve toward:

```text
ADK Agent
    ↓
MCP Client
    ↓
MCP Server
    ↓
Approved Banking Capability
    ↓
Service / Database
```

The project will explore:

- MCP host/client/server concepts
- MCP tools
- MCP resources
- Tool schemas
- Transport mechanisms
- Capability discovery
- Tool invocation
- Error handling
- MCP integration testing
- Differences between MCP and conventional REST APIs

The goal is to use MCP for a real architectural responsibility rather than merely adding it as a technology keyword.

---

# LangChain

LangChain is planned for a **separate, justified responsibility** rather than duplicating Google ADK orchestration.

Potential responsibilities include:

- Policy retrieval
- Prompt composition
- Model abstraction
- Structured output
- Retrieval-Augmented Generation
- Document processing
- Context construction

A possible future flow is:

```text
ADK Agent
    ↓
determines policy research is required
    ↓
Policy capability
    ↓
LangChain retrieval pipeline
    ↓
Embedding search
    ↓
Relevant policy passages
    ↓
Structured grounded result
    ↓
ADK continues workflow
```

This separation keeps architecture responsibilities explicit.

---

# Retrieval-Augmented Generation (RAG)

Banking servicing frequently requires retrieving information from policies, procedures, knowledge bases, and servicing documentation.

The planned retrieval architecture is:

```text
Policy Documents
      ↓
Document Loading
      ↓
Chunking
      ↓
Embedding Model
      ↓
Vector Index
      ↓
Similarity Search
      ↓
Relevant Policy Context
      ↓
LLM
      ↓
Grounded Policy Response
```

Potential use cases include:

```text
"What does the synthetic policy say about
address verification failures?"
```

or:

```text
"What should happen when KYC documents
remain incomplete after the review period?"
```

The model should answer using retrieved policy evidence rather than relying purely on pretrained knowledge.

---

# Vector Search / Vector Database

A vector search layer may be introduced for semantic retrieval over synthetic banking policies and procedures.

Potential technologies will be evaluated based on project complexity and architectural need rather than added solely for technology coverage.

Possible options include:

- PostgreSQL + pgvector
- Chroma
- Qdrant
- another appropriate vector store

The final choice will be documented along with the architectural trade-offs.

---

# FastAPI

FastAPI is planned as the external application/API boundary.

Potential endpoints may include:

```text
POST /api/v1/agent/query
GET  /api/v1/customers/{customer_id}
GET  /api/v1/customers/{customer_id}/kyc
GET  /api/v1/cases/{case_id}
POST /api/v1/service-requests
GET  /health
```

FastAPI responsibilities will include:

- Request validation
- Pydantic schemas
- Authentication boundary
- Authorization
- Agent invocation
- Structured API responses
- Error handling
- Correlation/request IDs
- Health checks
- Logging
- API testing

The API layer will not delegate every deterministic request to the LLM unnecessarily.

---

# Data Storage

Different storage models will be selected based on the data being stored.

## PostgreSQL

Relational storage may be appropriate for:

- customers
- accounts
- service requests
- workflow states
- relationships requiring constraints
- auditable structured records

Potential technologies:

```text
PostgreSQL
SQLAlchemy
Alembic
```

## MongoDB / NoSQL

MongoDB may be evaluated for data that naturally benefits from document-oriented storage, such as:

- agent execution records
- nested workflow state
- flexible case metadata
- tool invocation traces
- semi-structured execution artifacts

MongoDB will only be added if the data model genuinely benefits from document-oriented storage.

---

# Asynchronous Workflows and Kafka

Not every banking operation should happen synchronously inside an HTTP request.

Long-running or event-driven workflows may eventually use:

```text
API / Agent
    ↓
Create task
    ↓
Event / Queue
    ↓
Worker
    ↓
Process workflow
    ↓
Persist result
    ↓
Status update
```

Potential use cases:

- KYC review requests
- document processing
- case creation
- downstream notifications
- audit-event processing
- long-running servicing workflows

The project may first implement a simpler queue abstraction before introducing Kafka.

If Kafka is introduced, the project will explore concepts such as:

- producers
- consumers
- topics
- events
- consumer groups
- retries
- dead-letter handling
- idempotency
- event schemas

Kafka will not be listed as implemented until an actual working event flow exists.

---

# Workflow Orchestration

The project distinguishes **agent reasoning** from **business workflow execution**.

A possible workflow:

```text
Request
   ↓
Understand intent
   ↓
Retrieve customer context
   ↓
Check KYC status
   ↓
Retrieve applicable policy
   ↓
Determine allowed next step
   ↓
Validate action
   ↓
Execute deterministic operation
   ↓
Persist result
   ↓
Audit
   ↓
Return structured response
```

Critical business actions should not rely solely on unconstrained LLM decisions.

The architecture will explore:

- deterministic rules
- workflow state
- retries
- timeouts
- idempotency
- failure recovery
- human escalation
- approval boundaries
- auditability

---

# Human-in-the-Loop

Some operations should require human review rather than autonomous execution.

Example:

```text
Agent identifies possible KYC discrepancy
               ↓
Agent gathers supporting evidence
               ↓
Agent summarizes case
               ↓
Deterministic policy determines
human approval is required
               ↓
Human reviewer
               ↓
Approved / rejected / escalated
```

The agent assists the workflow but does not automatically become the authority for high-risk decisions.

---

# Safety and Enterprise Controls

A production-oriented agent requires controls beyond prompting.

The project will progressively explore:

### Grounding

Agent responses should be based on approved tools and retrieved sources.

### Tool authorization

The agent should only have access to capabilities required for its responsibility.

### Input validation

Tool arguments and API requests should be validated before execution.

### Output validation

Structured model output should be checked before being consumed by downstream systems.

### Prompt-injection resistance

Retrieved or user-provided content should not automatically gain authority over system instructions or tool permissions.

### Human approval

Sensitive or high-impact operations should support human review.

### Auditability

Important agent and tool actions should be traceable.

### Least privilege

Agents and tools should have the minimum required permissions.

### Data protection

Real customer PII is intentionally excluded from this project.

---

# Structured Outputs

Natural-language responses are useful for humans, but downstream software needs predictable structures.

Future agent responses may use schemas similar to:

```json
{
  "status": "success",
  "intent": "kyc_requirements",
  "customer_type": "individual",
  "message": "Required KYC documents retrieved.",
  "data": {
    "documents": [
      "government-issued photo ID",
      "proof of address",
      "tax identification document"
    ]
  },
  "source": "synthetic_demo_policy",
  "requires_human_review": false
}
```

Pydantic models will be used where appropriate for validation and typed interfaces.

---

# Testing Strategy

Testing is treated as part of the agent architecture rather than an afterthought.

The project will distinguish between:

```text
Unit Tests
     ↓
Integration Tests
     ↓
Agent Evaluations
     ↓
End-to-End Tests
```

## Current Unit Tests

The deterministic KYC tool currently tests:

- individual KYC requirements
- business KYC requirements
- unsupported customer type
- customer-type normalization

Run:

```bash
python -m pytest -v
```

Current result:

```text
4 passed
```

## Planned Testing

Future tests will cover:

- API validation
- tool invocation
- MCP server behavior
- MCP client/server integration
- routing
- malformed model output
- tool failures
- unavailable dependencies
- invalid arguments
- unauthorized operations
- workflow transitions
- retrieval grounding
- agent behavior
- regression scenarios

Deterministic logic will primarily use ordinary unit tests.

Probabilistic model behavior will use targeted agent evaluations rather than assuming exact string equality.

---

# Observability

Agent systems introduce failure modes that ordinary application logs alone may not explain.

Planned observability includes:

- request IDs
- session IDs
- agent execution IDs
- tool invocation logs
- tool latency
- model latency
- model/token usage
- errors
- retries
- workflow transitions
- structured audit events

A conceptual trace might look like:

```text
request_id=REQ-101
session_id=SES-44
intent=kyc_status
tool=get_kyc_status
tool_latency_ms=42
model_latency_ms=830
status=success
```

Sensitive information should not be indiscriminately written to logs.

---

# Reliability

The project will explore production failure scenarios such as:

- LLM unavailable
- tool unavailable
- MCP server unavailable
- malformed model output
- timeout
- database failure
- duplicate request
- invalid customer identifier
- unsupported operation
- partial workflow failure

Relevant techniques include:

- explicit exceptions
- retries with limits
- timeouts
- idempotency
- fallback behavior
- structured error responses
- circuit-breaking concepts
- human escalation

---

# Cost and Latency

An agent should not invoke an LLM simply because an LLM is available.

Example:

```text
Known structured request
        ↓
Direct deterministic API
        ↓
No LLM required
```

For an ambiguous request:

```text
Natural-language request
        ↓
LLM interpretation
        ↓
Deterministic tool execution
        ↓
Grounded response
```

This separation can improve:

- reliability
- latency
- cost
- auditability
- testability

Model/token usage will eventually be included in observability.

---

# Docker and Deployment

The project is planned to become containerized after the core architecture is stable.

Potential services may eventually include:

```text
api
agent-service
mcp-server
postgres
vector-store
worker
message-broker
```

Docker / Docker Compose may be used for reproducible local development.

Cloud deployment will be considered only after the application is sufficiently complete to justify it.

---

# Project Structure

Current structure:

```text
ai-banking-servicing-agent/
│
├── app/
│   ├── __init__.py
│   └── agent.py
│
├── tests/
│   └── test_kyc_tools.py
│
├── docs/
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

The structure will evolve as responsibilities become large enough to separate.

A possible future structure is:

```text
ai-banking-servicing-agent/
│
├── app/
│   ├── agents/
│   ├── api/
│   ├── tools/
│   ├── services/
│   ├── workflows/
│   ├── models/
│   ├── schemas/
│   ├── retrieval/
│   ├── mcp/
│   ├── persistence/
│   ├── observability/
│   └── core/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── evals/
│
├── docs/
│
├── docker/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

The project will be refactored toward this structure only as the implementation requires it.

---

# Technology Roadmap

| Technology / Concept | Purpose | Status |
|---|---|---|
| Python 3.12 | Core backend language | ✅ Implemented |
| Google ADK | Agent development and orchestration | ✅ Implemented |
| Gemini 3.6 Flash | Agent LLM | ✅ Implemented |
| Deterministic tools | Authoritative banking capabilities | ✅ Implemented |
| Pytest | Automated testing | ✅ Implemented |
| Tool grounding | Reduce unsupported model claims | ✅ Implemented |
| ADK Runner | Agent execution lifecycle | 🔄 Next |
| ADK Session | Conversation/session management | 🔄 Next |
| ADK State | Stateful agent workflows | 🔄 Next |
| Pydantic | Typed structured validation | 📋 Planned |
| Additional banking tools | Multi-capability agent | 📋 Planned |
| MCP | Standardized capability interface | 📋 Planned |
| LangChain | Retrieval / model application components | 📋 Planned |
| FastAPI | External API layer | 📋 Planned |
| RAG | Grounded policy retrieval | 📋 Planned |
| Embeddings | Semantic policy representation | 📋 Planned |
| Vector search | Policy similarity retrieval | 📋 Planned |
| PostgreSQL | Relational persistence | 📋 Planned |
| MongoDB | Document persistence if justified | 📋 Evaluation |
| Queue / worker | Async processing | 📋 Planned |
| Kafka | Event streaming if justified | 📋 Evaluation |
| Authentication / RBAC | Access control | 📋 Planned |
| Human-in-the-loop | High-risk workflow review | 📋 Planned |
| Observability | Logs, traces, latency, usage | 📋 Planned |
| Docker | Reproducible runtime | 📋 Planned |
| Cloud deployment | Hosted environment | 📋 Future |

Legend:

```text
✅ Implemented
🔄 Next / In Progress
📋 Planned / Evaluation
```

---

# Development Roadmap

## Phase 1 — Google ADK Fundamentals

- [x] Create ADK agent
- [x] Connect Gemini model
- [x] Create deterministic banking tool
- [x] Register tool with agent
- [x] Execute tool from natural-language request
- [x] Add grounding instructions
- [x] Test unsupported information behavior
- [x] Add deterministic unit tests
- [ ] Runner
- [ ] Session
- [ ] State
- [ ] Multiple tools
- [ ] Structured outputs
- [ ] Callbacks / guardrails
- [ ] Error handling
- [ ] Agent evaluations

## Phase 2 — Banking Capabilities

- [ ] Synthetic customer profiles
- [ ] KYC status
- [ ] Onboarding status
- [ ] Service requests
- [ ] Case status
- [ ] Policy lookup
- [ ] Multi-step servicing scenarios

## Phase 3 — MCP

- [ ] Create MCP server
- [ ] Expose banking tools
- [ ] Build MCP client
- [ ] Connect ADK to MCP
- [ ] Validate schemas
- [ ] Handle MCP failures
- [ ] Add integration tests

## Phase 4 — LangChain and Retrieval

- [ ] Synthetic policy corpus
- [ ] Document loading
- [ ] Chunking
- [ ] Embeddings
- [ ] Vector search
- [ ] Retrieval pipeline
- [ ] Structured policy answers
- [ ] Citation / provenance handling
- [ ] Retrieval tests

## Phase 5 — FastAPI

- [ ] API application
- [ ] Pydantic request/response models
- [ ] Agent endpoint
- [ ] Deterministic endpoints where appropriate
- [ ] Error handling
- [ ] Health endpoint
- [ ] Authentication
- [ ] Authorization
- [ ] API tests

## Phase 6 — Persistence and Workflow

- [ ] Relational persistence
- [ ] Workflow state
- [ ] Idempotent service requests
- [ ] Audit records
- [ ] Evaluate MongoDB
- [ ] Async workers
- [ ] Evaluate Kafka / event streaming
- [ ] Retry and failure workflows

## Phase 7 — Production Engineering

- [ ] Structured logging
- [ ] Tracing
- [ ] Token / model usage
- [ ] Latency metrics
- [ ] Tool observability
- [ ] Agent evaluations
- [ ] Security review
- [ ] Prompt-injection testing
- [ ] Human approval
- [ ] Docker
- [ ] Integration test suite
- [ ] Architecture documentation

---

# Example Target Scenario

A future version of the platform should be able to handle a request such as:

```text
"Customer CUST-1001 says their onboarding has been
stuck for several days. Find out what's blocking it,
check the applicable policy, and tell me what should
happen next."
```

A possible execution plan:

```text
User Request
     ↓
Agent interprets goal
     ↓
get_customer_profile(CUST-1001)
     ↓
get_kyc_status(CUST-1001)
     ↓
Agent identifies blocking condition
     ↓
search_policy(blocking_condition)
     ↓
Retrieve grounded policy
     ↓
Determine permitted next action
     ↓
Human approval if required
     ↓
create_service_request(...)
     ↓
Persist + audit
     ↓
Structured response
```

The final answer should distinguish between:

- verified facts
- retrieved policy
- agent reasoning
- performed actions
- recommended actions
- actions requiring human approval

---

# Engineering Questions This Project Explores

This project is intentionally designed to answer practical AI-engineering questions:

- When should an LLM be used instead of deterministic software?
- When is an agent unnecessary?
- How should an agent select tools?
- How should authoritative tool output constrain an LLM?
- What happens when the tool does not contain enough information?
- How should agent state be managed?
- When should workflows be deterministic rather than agentic?
- What should MCP provide that REST does not?
- How should LangChain and Google ADK have separate responsibilities?
- When is RAG preferable to relying on model knowledge?
- Which data belongs in relational vs document storage?
- When does asynchronous processing become necessary?
- When is Kafka justified?
- How should tool failures be handled?
- How should high-risk actions require human approval?
- How can agent behavior be tested when model outputs are probabilistic?
- How should model/tool execution be audited?
- How can token usage and latency be controlled?
- How do we prevent an agent from exceeding its authority?

---

# Current Learning Milestone

The current milestone demonstrates an important distinction:

```text
LLM
│
├── understands natural language
├── selects an appropriate capability
└── communicates results
        │
        ▼
Deterministic Tool
│
├── validates input
├── retrieves authoritative synthetic data
└── returns structured output
```

The first implementation also demonstrated that **tool grounding must extend beyond tool invocation to the final generated response**.

This principle will remain central as the project evolves into multi-tool workflows.

---

# Running the Current Project

Create and activate a Python 3.12 virtual environment.

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Configure environment variables using `.env`.

Never commit real API keys.

Run the ADK agent:

```powershell
adk run app
```

Example:

```text
[user]:
What KYC documents are required for an individual customer?
```

Run tests:

```powershell
python -m pytest -v
```

---

# Security Notice

This repository is designed exclusively around synthetic banking scenarios.

Do not:

- store real customer information
- commit API keys
- use real account credentials
- use real KYC documents
- connect unauthorized banking systems
- treat generated responses as actual financial or compliance advice

The project is an AI engineering demonstration, not a production banking application.

---

# Key Takeaway

The long-term goal is not to build:

```text
LLM → everything
```

It is to build:

```text
                 AI Reasoning
                      │
                      ▼
               Controlled Agent
                      │
         ┌────────────┼────────────┐
         ▼            ▼            ▼
   Deterministic   Retrieval    Workflows
      Tools
         │            │            │
         └────────────┼────────────┘
                      ▼
              Authoritative Systems
                      │
                      ▼
          Validation / Audit / Humans
```

The project explores how modern agentic AI can complement traditional backend engineering while preserving reliability, grounding, security, auditability, and deterministic control.

---

## Disclaimer

This project uses synthetic banking data and simulated banking workflows for educational and portfolio purposes only. It is not affiliated with, endorsed by, or connected to any financial institution.