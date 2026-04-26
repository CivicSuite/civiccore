# CivicCore User Manual

Version: v0.2.0
Repository: https://github.com/CivicSuite/civiccore
License: Apache 2.0

This manual has three audiences. Read the section for your role.

1. **Non-technical overview for evaluators** — what civiccore is and why it
   exists.
2. **Technical guide for module developers and IT integrators** — install,
   consume the public API, run civiccore migrations from a downstream
   alembic chain.
3. **Architecture reference** — shipped submodules (migration runner,
   shared `Base`, LLM provider registry, prompt-template engine, model
   registry, context utilities, structured output), the list of planned
   placeholder namespaces, and a text diagram of how they fit together.

---

## 1. Non-technical overview for evaluators

### What is CivicCore?

CivicCore is a **shared platform library** that sits underneath every product
in the CivicSuite family. The CivicSuite family is a set of open-source
municipal operations applications — the first one shipped is **CivicRecords AI**,
a public-records request management app for city governments. Future
modules (CivicClerk, CivicCode, CivicZone) will follow.

Rather than each of those apps re-inventing the same plumbing, CivicCore
provides one shared, audited, semver-stable implementation that each
module imports.

**What v0.2.0 actually ships:**

- `civiccore.migrations` — migration runner with idempotent guards plus
  the `civiccore_0001_baseline_v1` shared-schema baseline and the
  `civiccore_0002_llm` Phase 2 ALTER.
- `civiccore.db` — shared SQLAlchemy declarative `Base`.
- `civiccore.llm` — LLM provider abstraction (Ollama / OpenAI /
  Anthropic), prompt template engine with 3-step override resolver, model
  registry service + admin router, context utilities with prompt-injection
  defense, and Pydantic-validated structured output.

**Planned extraction targets (not yet implemented).** The following
namespaces have placeholder `__init__.py` files reserving the import path
but ship no implementation in v0.2.0: `civiccore.audit`, `civiccore.auth`,
`civiccore.catalog`, `civiccore.connectors`, `civiccore.exemptions`
(50-state public-records exemption engine), `civiccore.ingest` (document
ingestion), `civiccore.notifications`, `civiccore.onboarding`,
`civiccore.scaffold`, `civiccore.search` (hybrid search), and
`civiccore.verification` (sovereignty verification). These will land in
future Phase releases and must not be relied on by downstream modules
until they do.

### What CivicCore is not

CivicCore is **not** an end-user application. A city clerk does not "install
CivicCore." A resident does not "log in to CivicCore." CivicCore is a
library that the actual end-user apps depend on.

### Who consumes CivicCore today

- **CivicRecords AI v1.4.0** — public-records request management app. Uses
  civiccore v0.2.0 for LLM provider access, prompt templates, model
  registry, and the shared migration baseline.

### Who will consume CivicCore next

- **CivicClerk** — meeting management and agenda packets.
- **CivicCode** — code enforcement.
- **CivicZone** — zoning and permits.

These modules are on the CivicSuite roadmap; civiccore's API is designed so
they can plug in without civiccore changing shape.

### Why this exists

Three reasons:

1. **Sovereignty.** Cities can run the entire stack on their own
   infrastructure (Ollama, local PostgreSQL) without vendor lock-in.
   CivicCore's LLM abstraction makes the local-first deployment the default
   path; cloud providers (OpenAI, Anthropic) are opt-in.
2. **Reuse without coupling.** Each CivicSuite module gets a stable,
   versioned dependency surface — not a tangle of cross-imports.
3. **Audit and compliance.** Plumbing that touches resident data
   (logging, sanitization, prompt-injection defense) lives in one place
   where it can be reviewed and tested.

### Where CivicCore is in its lifecycle

Phase 2 has shipped. v0.2.0 is the second public release. There is no PyPI
release yet — civiccore is distributed as GitHub release wheels, signed
with SHA-256 checksums.

---

## 2. Technical guide for module developers and IT integrators

### Audience

You are writing or operating a CivicSuite module (an app like records-ai),
or you are an IT integrator standing one up for a city. You need to install
civiccore as a dependency, consume its public API, and run its migrations.

### Install (from a release wheel)

CivicCore is distributed as versioned GitHub release wheels — **not on
PyPI**. Pin the exact wheel URL in your downstream project:

    pip install https://github.com/CivicSuite/civiccore/releases/download/v0.2.0/civiccore-0.2.0-py3-none-any.whl

Each release publishes `SHA256SUMS.txt` alongside the wheel and sdist:

    curl -L -o SHA256SUMS.txt \
      https://github.com/CivicSuite/civiccore/releases/download/v0.2.0/SHA256SUMS.txt
    sha256sum -c SHA256SUMS.txt

Always verify the checksum before promoting an artifact into a downstream
module or an internal package mirror.

### Optional cloud-provider SDKs

The Ollama provider is built in and uses `httpx` (already a base dependency).
OpenAI and Anthropic providers require their respective SDKs and are
installed only if you intend to use them:

    pip install openai      # only if instantiating OpenAIProvider
    pip install anthropic   # only if instantiating AnthropicProvider

### Consuming the LLM provider abstraction

```python
from civiccore.llm import (
    get_provider,
    register_provider,
    LLMProvider,
)

provider = get_provider("ollama", base_url="http://localhost:11434")
text = await provider.generate(
    system_prompt="You summarize public-records requests.",
    user_content="Summarize this request: ...",
)
```

Register a custom provider without modifying civiccore source:

```python
from civiccore.llm import LLMProvider, register_provider

@register_provider("my_provider")
class MyProvider(LLMProvider):
    async def generate(self, *, system_prompt, user_content, **kwargs):
        ...
```

### Consuming the prompt template engine

```python
from civiccore.llm import (
    resolve_template,
    render_template,
)

# 3-step resolver: app DB override → code-level override → civiccore default
template = await resolve_template(
    session,
    template_name="extract_request_fields",
    consumer_app="records-ai",
)
rendered = render_template(template, {"document_text": doc})
```

The 3-step resolver lets operators hot-fix a prompt in production via the
DB without re-deploying code, while preserving a code-level override for
deterministic test environments and a civiccore default as a safe fallback.

### Consuming the model registry

```python
from civiccore.llm import (
    get_active_model,
    require_active_model,
    model_registry_router,
)
from fastapi import FastAPI

app = FastAPI()
app.include_router(model_registry_router, prefix="/admin/models")

active = await require_active_model(session, role="extraction")
```

### Running civiccore migrations from a downstream alembic chain

CivicCore ships a baseline migration `civiccore_0001_baseline_v1` that
creates the shared schema (prompt_templates, model_registry, llm_audit
tables, etc.). Downstream consumers run civiccore's migrations as part of
their own alembic chain by depending on civiccore's version table.

Pattern:

    # In your downstream module's alembic env.py:
    from civiccore.migrations import include_civiccore_migrations
    include_civiccore_migrations(context)

    # Then your module's revisions can list civiccore_0001_baseline_v1 as
    # a `down_revision` dependency, ensuring civiccore's tables exist
    # before your module's tables reference them.

For the canonical pattern, look at `civicrecords-ai`'s `alembic/env.py` —
it is the reference integration.

### Operating notes

- **Idempotent.** Migration application is idempotent; safe to re-run.
- **No network at import time.** Importing `civiccore.llm` does not make
  any LLM calls. Provider construction is the first network event.
- **No cost tracking.** Per ADR-0004, civiccore does not track LLM spend.
  Token counting in `civiccore.llm` is for context-window math only.
- **Sovereignty default.** Ollama is the default provider in the registry.
  OpenAI and Anthropic must be explicitly enabled by the operator.

---

## 3. Architecture reference

### Submodules

Shipped (have implementation in v0.2.0):

```
civiccore/
├── db/                  # Shared SQLAlchemy declarative Base
├── migrations/          # Migration runner + civiccore_0001_baseline_v1
│                        # + civiccore_0002_llm Phase 2 ALTER
└── llm/                 # The civiccore.llm module (Phase 2)
    ├── providers/       # LLMProvider ABC + Ollama / OpenAI / Anthropic
    ├── factory.py       # build_provider() + CONFIG_SCHEMAS
    ├── templates/       # PromptTemplate ORM + render + 3-step resolver
    ├── registry/        # ModelRegistry ORM + service + admin router
    ├── context.py       # TokenBudget, assemble_context, sanitize_for_llm
    └── structured.py    # StructuredOutput (Pydantic-validated retry)
```

Planned (placeholder packages exist; implementation is future Phase work):

```
civiccore/
├── audit/               # placeholder — future audit logging
├── auth/                # placeholder — future authentication
├── catalog/             # placeholder — future catalog primitives
├── connectors/          # placeholder — future external connectors
├── exemptions/          # placeholder — future 50-state exemption engine
├── ingest/              # placeholder — future document ingestion
├── notifications/       # placeholder — future notification primitives
├── onboarding/          # placeholder — future onboarding flows
├── scaffold/            # placeholder — future scaffolding helpers
├── search/              # placeholder — future hybrid search
└── verification/        # placeholder — future sovereignty verification
```

Each placeholder directory contains only an `__init__.py` docstring stub.
These namespaces are reserved import paths, not capability — do not
import from them in downstream code until they ship.

### How CivicCore fits with downstream consumers

```
+---------------------------------------------------------------+
|                  Downstream consumer (e.g. records-ai)        |
|                                                               |
|   FastAPI app   alembic chain   business logic   UI           |
|        |              |               |                       |
+--------|--------------|---------------|-----------------------+
         |              |               |
         |              |               |  imports
         v              v               v
+---------------------------------------------------------------+
|                       civiccore (library)                     |
|                                                               |
|   civiccore.llm                  civiccore.migrations         |
|     - provider registry           - runner                    |
|     - prompt templates            - civiccore_0001_baseline   |
|     - model registry             civiccore.db                 |
|     - context utils               - shared declarative Base   |
|     - structured output                                       |
|                                                               |
+---------------------------------------------------------------+
         |              |               |
         v              v               v
+---------------------------------------------------------------+
|              External services (operator-controlled)          |
|                                                               |
|   Ollama (default)   PostgreSQL    OpenAI*    Anthropic*      |
|                                                               |
|   * opt-in; require explicit registry entry + SDK install     |
+---------------------------------------------------------------+
```

### Migration ordering contract

CivicCore migrations are designed to run **before** any downstream
consumer's migrations. Downstream consumers reference civiccore's tables
in foreign keys and must list `civiccore_0001_baseline_v1` (or a later
civiccore revision) as a `down_revision`.

The migration runner uses idempotent guards — re-running a migration that
has already been applied is a no-op, not a failure.

### Provider abstraction

```
LLMProvider (ABC)
   |
   +-- OllamaProvider          (built-in, default; uses httpx)
   +-- OpenAIProvider          (built-in; opt-in; pip install openai)
   +-- AnthropicProvider       (built-in; opt-in; pip install anthropic)
   +-- (third-party providers via @register_provider)
```

Construction goes through `build_provider(config)` (the factory) or
`get_provider(name, **kwargs)` (the registry shortcut). The ABC defines an
async `generate(system_prompt, user_content, **kwargs)` contract; concrete
providers implement transport, auth, and serialization details.

### Prompt template 3-step resolver

```
resolve_template(session, name, consumer_app)

   1. App DB override
        consumer_app=<requesting app>
        is_override=True, is_active=True, highest version

   2. App code-level override
        OVERRIDE_REGISTRY[(consumer_app, name)]
        registered via register_template_override()

   3. CivicCore default
        consumer_app="civiccore"
        is_override=False, is_active=True, highest version

   else: PromptTemplateNotFoundError
```

DB overrides win over code overrides so operators retain production
hot-fix capability without a code deploy.

### Context utilities and structured output

`assemble_context()` packs system prompt + retrieved chunks into a
token-budgeted prompt, applying `sanitize_for_llm()` at chunk boundaries
to defuse prompt-injection attempts in retrieved content. `StructuredOutput`
wraps a provider call with a Pydantic schema; if the model returns
malformed JSON, it retries up to `max_attempts` times before raising
`StructuredOutputFailure`.

### Sovereignty and ADR-0004

- No cost tracking, no spend limits in civiccore.
- No telemetry; no phone-home.
- Local-first default (Ollama).
- Cloud providers are opt-in and require an explicit registry entry.

For the full design rationale see CivicCore Extraction Spec section 12 and
ADR-0004 in the civicsuite umbrella repo.

---

## Appendix: Where to file issues

- **Bug in civiccore itself** — file at https://github.com/CivicSuite/civiccore/issues
- **Bug that surfaces in records-ai but is caused by civiccore** — file at civiccore.
- **Bug in records-ai** — file at https://github.com/CivicSuite/civicrecords-ai/issues
- **Suite-wide design / cross-module question** — file at https://github.com/CivicSuite/civicsuite/issues
- **Security vulnerability** — see SECURITY.md (do not file publicly).

The decision tree in CONTRIBUTING.md has the full rules.
