CivicCore
=========

Shared platform library for the CivicSuite open-source municipal operations
suite. https://github.com/CivicSuite/civicsuite

What this is
------------

CivicCore is the Python library every CivicSuite module depends on for
authentication, audit logging, LLM access, document ingestion, hybrid
search, connectors, notifications, onboarding, the 50-state public-records
exemption engine, and sovereignty verification. It is extracted from the
production CivicRecords AI codebase per the CivicCore Extraction Spec and is
consumed today by CivicRecords AI v1.4.0; CivicClerk, CivicCode, and
CivicZone will consume it as they ship.

CivicCore is a library, not an end-user municipal app.

Status
------

Phase 2 shipped. v0.2.0 ships the civiccore.llm module: provider abstraction
(Ollama / OpenAI / Anthropic with ABC + factory), prompt template engine
with a 3-step override resolver, model registry service + admin router,
context utilities with prompt-injection defense, and a Pydantic-validated
structured-output helper. v0.1.0 was the Phase 1 baseline (migration runner,
idempotent guards, and the civiccore_0001_baseline_v1 shared-schema baseline
extracted from CivicRecords AI).

Install
-------

From the GitHub release wheel:

    pip install https://github.com/CivicSuite/civiccore/releases/download/v0.2.0/civiccore-0.2.0-py3-none-any.whl

CivicCore is distributed as versioned GitHub release artifacts (not on PyPI).

For development from a clone:

    git clone https://github.com/CivicSuite/civiccore.git
    cd civiccore
    pip install -e .[dev]

Each release publishes SHA256SUMS.txt alongside the wheel and sdist. Verify
checksums before promoting an artifact downstream.

Public API surface (high level)
-------------------------------

  civiccore.llm
    LLMProvider, register_provider, get_provider, list_providers
    OllamaProvider, OpenAIProvider, AnthropicProvider, build_provider
    PromptTemplate, RenderedPrompt, render_template, resolve_template
    ModelRegistry, model_registry_router, get_active_model
    TokenBudget, ContextBlock, assemble_context, blocks_to_prompt
    sanitize_for_llm, StructuredOutput, StructuredOutputFailure

  civiccore.migrations
    Migration runner + civiccore_0001_baseline_v1 shared schema

  civiccore.db
    Base (shared SQLAlchemy declarative base)

The full enumerated list lives in civiccore/llm/__init__.py and Appendix A
of the CivicCore Extraction Spec. Anything not in Appendix A is internal and
subject to change.

Compatibility
-------------

civicrecords-ai v1.4.0 consumes civiccore v0.2.0. The suite-wide
compatibility matrix is maintained at
https://github.com/CivicSuite/civicsuite/tree/main/docs/compatibility

License
-------

Apache License 2.0. See LICENSE.

Contributing
------------

See CONTRIBUTING.md, including the decision tree for where to file a bug
across the CivicSuite multi-repo layout.

Source
------

https://github.com/CivicSuite/civiccore
