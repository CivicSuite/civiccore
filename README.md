# CivicCore

Shared platform package for the
[CivicSuite](https://github.com/CivicSuite/civicsuite) open-source
municipal operations suite.

## What this is

CivicCore is the Python package every CivicSuite module depends on for
authentication, audit logging, LLM access, document ingestion, hybrid
search, connectors, notifications, onboarding, the 50-state public-records
exemption engine, and sovereignty verification. It is extracted from the
production CivicRecords AI codebase per the CivicCore Extraction Spec, and
is consumed today by CivicRecords AI; CivicClerk, CivicCode, and CivicZone
will consume it as they ship.

## Status

**Phase 1 shipped.** `v0.1.0` is the first functional CivicCore release:
the migration runner, idempotent guards, and the `civiccore_0001_baseline_v1`
shared-schema baseline extracted from CivicRecords AI. See the CivicCore
Extraction Spec section 12 for the phased rollout.

## Install

From the GitHub release wheel:

```bash
pip install https://github.com/CivicSuite/civiccore/releases/download/v0.1.0/civiccore-0.1.0-py3-none-any.whl
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

PyPI publication can come later; `v0.1.0` is distributed first as a versioned
GitHub release artifact so CivicRecords AI can stop depending on a Git SHA pin.
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
    resolve_template,           # async DB resolver (2-step override)
    CIVICCORE_DEFAULT_APP,      # "civiccore" namespace constant
    PromptTemplateError,        # exceptions
    PromptTemplateNotFoundError,
    PromptTemplateRenderError,
)
```

### Resolution order

`resolve_template(session, template_name=..., consumer_app=...)` returns the active `PromptTemplate` row using:

1. **App override** — `consumer_app=<requesting app>`, `is_override=True`, `is_active=True`, highest `version`.
2. **CivicCore default** — `consumer_app="civiccore"`, `is_override=False`, `is_active=True`, highest `version`.
3. Otherwise raises `PromptTemplateNotFoundError`.

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

## Public API surface

After Step 3, `civiccore.llm` exposes a single import surface for downstream apps:

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

Every CivicSuite module's README declares a CivicCore version range
(e.g. `civiccore >= 0.1, < 0.2`). The suite-wide compatibility matrix —
which module versions work with which CivicCore versions — is maintained
at
[CivicSuite/civicsuite/docs/compatibility/](https://github.com/CivicSuite/civicsuite/tree/main/docs/compatibility).

## License

[Apache License 2.0](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md), including the decision tree for
where to file a bug across the CivicSuite multi-repo layout.
