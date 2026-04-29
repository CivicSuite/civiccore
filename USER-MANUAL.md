# CivicCore User Manual

Version: v0.9.0 (development line; latest published release v0.8.0)
Repository: https://github.com/CivicSuite/civiccore
License: Apache 2.0

This manual has three audiences:

1. **Non-technical evaluators** - what CivicCore is and why it matters.
2. **IT and module developers** - how to install it and consume the public API.
3. **Architecture reviewers** - what ships today, what is planned, and how the library fits into the CivicSuite stack.

---

## 1. Non-Technical Overview

### What CivicCore Is

CivicCore is the shared platform library underneath CivicSuite. It is the common
Python package that CivicSuite modules use for migrations, LLM plumbing,
provenance metadata, audit-chain primitives, export manifests, and local city
configuration.

It is **not** an app a clerk or resident logs into. End users interact with
module applications such as CivicRecords AI or CivicClerk. CivicCore is the
shared foundation those applications import.

### What the current development line ships

- `civiccore.migrations` - migration runner, idempotent guards, and the shared
  schema baseline.
- `civiccore.db` - shared SQLAlchemy declarative `Base`.
- `civiccore.llm` - provider registry, prompt templates, model registry,
  context utilities, and structured-output helpers.
- `civiccore.audit` - hash-chained audit primitives for tamper-evident local
  event streams.
- `civiccore.provenance` - source, citation, document, and provenance metadata
  contracts.
- `civiccore.connectors` - offline import/export manifest schemas plus
  local-first import helpers for supported agenda-platform payloads.
- `civiccore.exports` - static export-bundle manifest and checksum helpers.
- `civiccore.city_profile` - local city/deployment configuration models.
- `civiccore.auth` - bearer-token role helpers for protected or mixed
  public/staff FastAPI routes.
- `civiccore.verification` - content-bound browser release-evidence helpers.
- `civiccore.search` - deterministic text normalization, matching, and
  reciprocal-rank-fusion helpers.
- `civiccore.notifications` - notice deadline planning and publication
  compliance helpers with actionable warning codes.

### What the current development line does not ship yet

The following namespaces remain planned extraction targets:
`civiccore.catalog`, `civiccore.exemptions`, `civiccore.ingest`,
`civiccore.onboarding`, and `civiccore.scaffold`.

Live connector sync, credential storage, vendor write-back, document ingestion,
search indexing, notification delivery queues, and legal determinations are also not
shipped platform behaviors. Downstream modules must not promote those behaviors
as shipped CivicCore capability.

### Why Municipal Teams Should Care

- **Sovereignty:** Local-first defaults keep cities in control of their data and
  infrastructure.
- **Reuse without coupling:** Each CivicSuite module depends on the same
  versioned primitives rather than copying logic.
- **Auditability:** Shared contracts for provenance, export bundles, and audit
  chains make compliance evidence more consistent across modules.

---

## 2. Technical Guide for IT and Module Developers

### Install from a Release Wheel

CivicCore is distributed as GitHub release artifacts, not PyPI packages:

```bash
pip install https://github.com/CivicSuite/civiccore/releases/download/v0.8.0/civiccore-0.8.0-py3-none-any.whl
```

Each release publishes `SHA256SUMS.txt` next to the wheel and source
distribution. Verify checksums before promoting a release artifact:

```bash
curl -L -o SHA256SUMS.txt \
  https://github.com/CivicSuite/civiccore/releases/download/v0.8.0/SHA256SUMS.txt
sha256sum -c SHA256SUMS.txt
```

For local development:

```bash
git clone https://github.com/CivicSuite/civiccore.git
cd civiccore
pip install -e .[dev]
```

### Use LLM Providers

```python
from civiccore.llm import get_provider

provider = get_provider("ollama", base_url="http://localhost:11434")
text = await provider.generate(
    system_prompt="You summarize municipal records.",
    user_content="Summarize this request: ...",
)
```

Ollama uses the base dependency set. OpenAI and Anthropic require their SDKs
only if those providers are instantiated:

```bash
pip install openai
pip install anthropic
```

### Use Prompt Templates

```python
from civiccore.llm import render_template, resolve_template

template = await resolve_template(
    session,
    template_name="extract_request_fields",
    consumer_app="records-ai",
)
rendered = render_template(template, {"document_text": document_text})
```

The resolver checks app DB overrides first, code-level overrides second, and
CivicCore defaults third. Missing variables produce actionable render errors.

### Use Audit, Provenance, Manifest, Export, and City Profile Primitives

```python
from civiccore import (
    AuditActor,
    AuditHashChain,
    AuditSubject,
    CityProfile,
    ExportBundle,
    ImportManifest,
    SourceReference,
    validate_bundle,
    validate_manifest,
)

chain = AuditHashChain()
chain.record_event(
    actor=AuditActor(actor_id="clerk-1", actor_type="staff"),
    action="packet_exported",
    subject=AuditSubject(subject_id="meeting-42", subject_type="meeting"),
    source_module="civicclerk",
)
assert chain.verify()
```

These primitives are storage-neutral. They give downstream modules a consistent
contract without dictating where records are stored.

### Run Migrations from a Consumer

CivicCore migrations run before a downstream module's migrations. Consumer
modules use CivicCore's migration runner and keep their own version table so
revision names do not collide.

The release gate verifies the CivicCore migration chain, including
`civiccore_0001_baseline_v1` and `civiccore_0002_llm`.

---

## 3. Architecture Reference

### Shipped vs Planned

![CivicCore extraction map](docs/diagrams/civiccore-extraction-map.svg)

Shipped implementation in the current development line:

```text
civiccore/
  audit/        hash-chained audit primitives
  city_profile/ local city/deployment configuration models
  connectors/   offline manifests plus local-first import helpers
  db/           shared SQLAlchemy declarative Base
  exports/      static export-bundle helpers
  llm/          providers, templates, registry, context, structured output
  migrations/   migration runner and shared schema baseline
  notifications/ notice deadline + compliance helpers
  provenance/   source/citation/provenance metadata contracts
```

Still planned namespaces:

```text
civiccore/
  catalog/       future catalog primitives
  exemptions/    future 50-state public-records exemption engine
  ingest/        future document ingestion
  notifications/ delivery queues and outbound orchestration remain future work
  onboarding/    future web onboarding flows
  scaffold/      future scaffolding helpers
  verification/  future sovereignty verification
```

### Migration Order

![Migration order](docs/diagrams/migration-order.svg)

Consumer applications run CivicCore migrations first, then their own module
migrations. Separate Alembic version tables prevent revision-name collisions.

### LLM Provider Abstraction

![Provider abstraction](docs/diagrams/provider-abstraction.svg)

The provider abstraction keeps local Ollama as the sovereignty-first default
while allowing explicitly configured cloud providers where a city authorizes
them.

### Compatibility

Current v0.1.0 module foundations still pin older civiccore lines.
Production-depth consumers can move to `civiccore==0.9.0` after this release
and the suite compatibility matrix is updated.

The suite-wide matrix lives at:
https://github.com/CivicSuite/civicsuite/tree/main/docs/compatibility

---

## Appendix: Where to File Issues

- CivicCore bug: https://github.com/CivicSuite/civiccore/issues
- Suite-wide design issue: https://github.com/CivicSuite/civicsuite/issues
- Security issue: follow `SECURITY.md`; do not file publicly.

The decision tree in `CONTRIBUTING.md` has the full routing rules.
