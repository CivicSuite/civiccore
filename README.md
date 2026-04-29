# CivicCore

Shared platform package for the
[CivicSuite](https://github.com/CivicSuite/civicsuite) open-source
municipal operations suite.

## What this is

CivicCore is the Python package every CivicSuite module depends on for
shared platform plumbing. **What ships today:** the migration runner plus
`civiccore_0001_baseline_v1` shared-schema baseline, a shared SQLAlchemy
declarative `Base`, the `civiccore.llm` module, hash-chained audit
primitives, source/provenance metadata contracts, offline import/export
manifest schemas, static export-bundle helpers, local city profile
configuration, bearer-token role helpers for downstream FastAPI
services, including mixed public/staff routes that should stay anonymous
by default while unlocking privileged results for authorized callers,
browser-evidence verification helpers for current-facing release pages,
small shared search helpers for deterministic text matching plus
hybrid ranking fusion, and local-first connector import helpers for
agenda-platform payload normalization with actionable error contracts and
source provenance.

**Still planned extraction targets (placeholder packages exist; not yet
implemented today):** `civiccore.catalog`, `civiccore.exemptions`
(50-state public-records exemption engine),
`civiccore.ingest` (document ingestion), `civiccore.notifications`,
`civiccore.onboarding` (web onboarding flows), and
`civiccore.scaffold`. `civiccore.search` now ships normalization and
fusion helpers, but not a full search engine or indexer.
`civiccore.verification` now ships the first release-evidence helper
surface, while sovereignty verification remains future work.
`civiccore.connectors` now also ships shared local-payload import
normalization helpers for supported agenda platforms, but not live sync,
credential handling, or vendor write-back. Unshipped
namespaces are reserved for future Phase work and must not be relied on
by downstream modules until they ship.

## Status

**v0.8.0 is in development.** This line adds shipped
`civiccore.connectors` local-first import helpers for supported agenda
platform payloads, keeps the shipped `civiccore.search` helper surface
for deterministic text matching and reciprocal-rank-fusion, keeps the
shipped `civiccore.verification` release-evidence helpers, extends the
shipped `civiccore.auth` surface with an optional bearer resolver for
mixed public/staff endpoints, and keeps the shared audit, provenance,
manifest, export-bundle, and city profile primitives needed for the
first production-depth CivicSuite workflows. The most recent published
GitHub release is `v0.7.0`.
`v0.2.0` shipped the `civiccore.llm` module:
provider abstraction (Ollama / OpenAI / Anthropic), prompt template engine
with a 3-step override resolver, model registry service + admin router,
context utilities with prompt-injection defense, and a Pydantic-validated
structured-output helper. `v0.1.0` was the Phase 1 baseline (migration
runner, idempotent guards, and the `civiccore_0001_baseline_v1`
shared-schema baseline extracted from CivicRecords AI).

## Architecture

### Shipped vs placeholder

![civiccore extraction map](docs/diagrams/civiccore-extraction-map.svg)

### Migration order (consumer chain)

![Migration order](docs/diagrams/migration-order.svg)

### LLM provider abstraction

![Provider abstraction](docs/diagrams/provider-abstraction.svg)

## Install

From the current published GitHub release wheel (`v0.7.0`):

```bash
pip install https://github.com/CivicSuite/civiccore/releases/download/v0.7.0/civiccore-0.7.0-py3-none-any.whl
```

Each GitHub release also publishes `SHA256SUMS.txt` alongside the wheel and
sdist. Verify the checksum before promoting a release artifact into a downstream
module or internal package mirror.

For development from a clone:

```bash
git clone https://github.com/CivicSuite/civiccore.git
cd civiccore
pip install -e .[dev]
```

PyPI publication can come later; CivicCore is distributed as versioned
GitHub release artifacts so CivicRecords AI can stop depending on a Git SHA pin.
The tag-driven release workflow runs `scripts/verify-release.sh` before
publishing so the shipped artifact has already passed pytest, ruff,
docs/version checks, a local build, and a clean-virtualenv wheel-install smoke
test.

## LLM providers

CivicCore exposes a pluggable LLM provider abstraction for downstream apps. Three providers ship built-in:

```python
from civiccore.llm.providers import (
    LLMProvider,         # ABC
    register_provider,   # decorator for adding new providers
    get_provider,        # construct a provider by name
    list_providers,      # introspection
    OllamaProvider,
    OpenAIProvider,
    AnthropicProvider,
)

# Built-in usage
provider = get_provider("ollama", base_url="http://localhost:11434")
text = await provider.generate(system_prompt="...", user_content="...")
```

Optional cloud-provider SDKs are needed only if you instantiate the corresponding provider:

```bash
# Direct install (works today, including GitHub wheel installs):
pip install openai      # required for OpenAIProvider
pip install anthropic   # required for AnthropicProvider

# Extras shorthand (works once civiccore is published to PyPI):
pip install civiccore[openai]
pip install civiccore[anthropic]
```

Ollama needs no extra (uses httpx, already a base dependency).

Third-party providers register via the public decorator without modifying civiccore source:

```python
from civiccore.llm.providers import LLMProvider, register_provider

@register_provider("my_provider")
class MyProvider(LLMProvider):
    ...
```

## LLM templates

CivicCore exposes a prompt-template rendering and override-resolution layer for downstream apps.

```python
from civiccore.llm.templates import (
    PromptTemplate,             # ORM
    PromptTemplateCreate,       # Pydantic schemas
    PromptTemplateRead,
    RenderedPrompt,             # render() result dataclass
    render_template,            # string.Template renderer
    resolve_template,           # async DB resolver (3-step: app DB → code-level → civiccore default)
    CIVICCORE_DEFAULT_APP,      # "civiccore" namespace constant
    PromptTemplateError,        # exceptions
    PromptTemplateNotFoundError,
    PromptTemplateRenderError,
)
```

### Resolution order

`resolve_template(session, template_name=..., consumer_app=...)` returns the active `PromptTemplate` row using:

1. **App DB override** — `consumer_app=<requesting app>`, `is_override=True`, `is_active=True`, highest `version`.
2. **App code-level override** — in-memory `OVERRIDE_REGISTRY` populated via `register_template_override` (per ADR-0004 §7). DB overrides win over code overrides so operators retain production hot-fix capability.
3. **CivicCore default** — `consumer_app="civiccore"`, `is_override=False`, `is_active=True`, highest `version`.
4. Otherwise raises `PromptTemplateNotFoundError`.

Callers passing `consumer_app="civiccore"` skip both override steps (1 and 2) and resolve directly to the civiccore default.

### Rendering

`render_template(template, {"key": "value", ...})` substitutes `string.Template` placeholders (`$key` or `${key}`). Missing variables raise `PromptTemplateRenderError` naming the missing key.

## LLM context utilities and structured output

CivicCore exposes context-budgeting and structured-output helpers at the package root:

```python
from civiccore.llm import (
    TokenBudget, ContextBlock,
    estimate_tokens, count_tokens, sanitize_for_llm,
    assemble_context, blocks_to_prompt, DEFAULT_CONTEXT_WINDOW,
    StructuredOutput, StructuredOutputFailure,
)

# Token-budgeted prompt assembly with prompt-injection defense
blocks = assemble_context(
    system_prompt="You are a helpful assistant.",
    chunks=[document_text],
    max_context_tokens=4096,
)
prompt = blocks_to_prompt(blocks)

# Pydantic-validated structured output with retry-on-malformed
class ExtractedFields(BaseModel):
    name: str
    confidence: float

result = await StructuredOutput(ExtractedFields).generate(
    provider=get_provider("ollama"),
    system_prompt="Extract fields from the document.",
    user_content=document_text,
    max_attempts=3,
)
```

Per ADR-0004: token counting is context-window math; no cost tracking, no spend limits.

## Audit, provenance, manifests, exports, and city profiles

The current CivicCore development line adds storage-neutral primitives
for production-depth municipal workflows:

```python
from civiccore import (
    AuditActor, AuditSubject, AuditHashChain,
    SourceReference, SourceKind, CitationTarget, ProvenanceBundle,
    ImportManifest, ExportManifest, ManifestFile, validate_manifest,
    ExportBundle, BundleFile, write_manifest, build_sha256sums, validate_bundle,
    CityProfile, load_city_profile,
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

These APIs are deliberately offline-first. They do not provide JWT
issuance, SSO, user directories, live connector sync, credential storage,
document ingestion, search indexing, legal determinations, or vendor
write-back.

## Auth helper

`civiccore.auth` now exposes small bearer-token role helpers for
downstream FastAPI services that need to protect non-public internal
endpoints or support mixed public/staff routes without taking on a full
identity-provider dependency.

```python
from fastapi import Depends
from fastapi.security import HTTPBearer

from civiccore.auth import authorize_bearer_roles, resolve_optional_bearer_roles

bearer = HTTPBearer(auto_error=False)

def read_workpaper(credentials = Depends(bearer)) -> dict[str, str]:
    authorize_bearer_roles(
        credentials,
        service_name="CivicBudget",
        feature_name="persisted workpaper retrieval",
        token_roles_env_var="CIVICBUDGET_AUTH_TOKEN_ROLES",
        allowed_roles={"workpaper_reader", "budget_admin"},
    )
    return {"status": "ok"}


def search_archive(credentials = Depends(bearer)) -> dict[str, bool]:
    principal = resolve_optional_bearer_roles(
        credentials,
        service_name="CivicClerk",
        feature_name="archive search staff access",
        token_roles_env_var="CIVICCLERK_AUTH_TOKEN_ROLES",
        allowed_roles={"archive_reader", "clerk_admin", "city_attorney"},
    )
    return {"include_closed": principal is not None}
```

Set `CIVICBUDGET_AUTH_TOKEN_ROLES` to a JSON object that maps bearer
tokens to role strings or role lists:

```json
{
  "demo-reader-token": ["workpaper_reader"],
  "budget-admin-token": "workpaper_reader,budget_admin"
}
```

If the config is missing or malformed, CivicCore raises an actionable
`503`; missing or invalid bearer headers return `401`; tokens without an
allowed role return `403`. The optional resolver returns `None` for
anonymous callers, which lets public endpoints stay public until a caller
actually presents a bearer token.

## Verification helper

`civiccore.verification` now ships a small browser-evidence helper for
current-facing release pages. It binds a release screenshot manifest to
the normalized content hash of a rendered source file, which keeps
browser QA evidence honest across Windows and Linux checkouts.

```python
from pathlib import Path

from civiccore.verification import validate_release_browser_evidence

result = validate_release_browser_evidence(
    repo_root=Path("."),
    manifest_path=Path("docs/browser-qa/release-evidence.json"),
    expected_version="0.1.2",
)
print(result.reviewed_at)
```

## Public API surface

`civiccore.llm` exposes a single import surface for downstream apps:

```python
from civiccore.llm import (
    # Providers
    LLMProvider, register_provider, get_provider, list_providers,
    OllamaProvider, OpenAIProvider, AnthropicProvider,
    # Templates
    PromptTemplate, PromptTemplateCreate, PromptTemplateRead,
    RenderedPrompt, render_template, resolve_template,
    CIVICCORE_DEFAULT_APP, PromptTemplateError,
    PromptTemplateNotFoundError, PromptTemplateRenderError,
    # Model registry
    ModelRegistry, ModelRegistryCreate, ModelRegistryRead, ModelRegistryUpdate,
    model_registry_router, MissingModelError, ModelRegistryServiceError,
    get_active_model, require_active_model, get_active_model_context_window,
    # Context utilities
    TokenBudget, ContextBlock, estimate_tokens, count_tokens, sanitize_for_llm,
    assemble_context, blocks_to_prompt, DEFAULT_CONTEXT_WINDOW,
    # Structured output
    StructuredOutput, StructuredOutputFailure, DEFAULT_MAX_ATTEMPTS,
)
```

The full enumerated list — stable across the v0.x series per the spec's
semver policy — is also published in **Appendix A of the CivicCore
Extraction Spec** in
[CivicSuite/civicsuite](https://github.com/CivicSuite/civicsuite).

## Compatibility

Every CivicSuite module's README declares its CivicCore dependency contract.
Current v0.1.0 module foundations pin older civiccore lines. Production-depth
consumers can move to `==0.8.0` after that release is published and the
compatibility matrix is updated. The suite-wide compatibility matrix — which
module versions work with which CivicCore versions — is maintained at
[CivicSuite/civicsuite/docs/compatibility/](https://github.com/CivicSuite/civicsuite/tree/main/docs/compatibility).

## License

[Apache License 2.0](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md), including the decision tree for
where to file a bug across the CivicSuite multi-repo layout.
