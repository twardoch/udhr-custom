---
this_file: REVIEW/TODO-cod.md
---

# Repository Improvement Plan (Proposals)

This document proposes concrete, example-driven improvements to structure, tooling, validation, and documentation. It does not change code outside `REVIEW/`.

## Objectives

- Data quality: Validate all UDHR XMLs and maintain reliable indices.
- Reproducibility: One-command pipelines for fetching, indexing, transliteration, and merge steps.
- Developer experience: Modern Python tooling, logging, and clear CLI usage.
- Documentation: Practical examples and contribution pathways.

## High-Impact Improvements

1) Validation and CI
- Add GitHub Actions workflow to validate all `data/udhr/*.xml` and `data/udhr-manual/*.xml` against `data/udhr/schema.rng`.
- Verify `data/udhr/index.xml` and `data/udhr-manual/index.xml` consistency with the actual files.
- Lint YAML in `merged/` and `tools/` for schema consistency.

2) Unified CLI for Tools
- Wrap `tools/*.py` in a unified CLI: `udhrtool [command]` (index, fetch, transliterate, merge, validate).
- Provide structured logging (loguru) and rich console output; add `--verbose` flag.

3) Dependency and Runtime Modernization
- Switch to `uv` for environment management and dependency locking.
- Add `ruff` (lint+format), `mypy` (optional), and pre-commit hooks.

4) Documentation Refresh
- Expand README with end-to-end examples (fetch → validate → index → merge → translit → browse).
- Add CONTRIBUTING.md with dataset etiquette, naming conventions, and validation steps.
- Add CHANGELOG.md, PLAN.md, TODO.md, WORK.md to track progress.

5) Data Hygiene
- Ensure all XMLs include required metadata attributes; harmonize `key` naming.
- Deduplicate and compress overly large YAMLs in `merged/` (keep normalized single source + reproducible pipelines).

## Detailed Plan (Phased)

Phase 1 — Validation & Index Health
- Implement `tools/validate_xml.py` to validate XMLs using lxml + RELAX NG.
- Implement `tools/verify_index.py` to assert that every `udhr_*.xml` is represented in the relevant index and vice versa.
- Add GitHub Actions: `ci.yml` with jobs: setup Python, install deps, run validation and index checks.

Phase 2 — Unified CLI & Logging
- Create `tools/cli.py` exposing subcommands: `validate`, `index`, `fetch`, `transliterate`, `merge`, `summarize`.
- Internals: reuse current scripts as modules; add loguru logging and `--verbose`.
- Example: `uv run python -m tools.cli validate --paths data/udhr data/udhr-manual`.

Phase 3 — Environment & Quality Gate
- Add `pyproject.toml` with ruff and mypy configs; configure `uv` project and lockfile.
- Add pre-commit hooks: ruff, end-of-file-fixer, trailing-whitespace, yaml-lint.
- Migrate `tools/requirements.txt` into `pyproject.toml` (keep the txt as a mirror for now).

Phase 4 — Documentation & Examples
- Expand README with runnable snippets:
  - “Validate all XMLs”: example command and sample output.
  - “Generate index.xml for curated set”: command + diff preview.
  - “Transliterate sample”: before/after text snippet.
- Add CONTRIBUTING.md with step-by-step: fork, branch, add XML, validate, open PR.
- Add repository maps in `REVIEW/FILES-cod.md` and keep updated via a small script.

Phase 5 — Data Normalization & Merges
- Normalize `merged/*.yaml` into one canonical `merged/udhr-art1.yaml` with provenance fields and versioned releases.
- Add `tools/merge_omniglot.py` that reproducibly re-generates the merged file from sources, documented in README.
- Add checks to ensure all language codes map to ISO identifiers consistently.

## Design Details & Examples

CLI layout (illustrative):

```
udhrtool
  validate        Validate XMLs against schema
  index           Rebuild index.xml for a folder
  fetch           Refresh official/r12a sources to YAML
  transliterate   Run Aksharamukha/Gimeltra batches
  merge           Rebuild merged YAML from sources
  summarize       Quick stats: files, langs, scripts, coverage
```

Example commands:

- Validate all XMLs and indices:
  - uv run python -m tools.cli validate --paths data/udhr data/udhr-manual
  - uv run python -m tools.cli index --path data/udhr-manual

- Rebuild merged Article 1 dataset:
  - uv run python -m tools.cli merge --sources tools/udhr_art1_official.yaml tools/udhr_art1_r12a.yaml --out merged/udhr-art1.yaml

- Transliterate a subset:
  - uv run python -m tools.cli transliterate --input data/udhr/udhr_san.xml --scheme aksharamukha --target Sidd

Logging conventions:

- Default: concise info-level progress; with `--verbose`, include per-file validation results and timing.
- Fail-fast with clear remediation tips; optionally `--continue-on-error` for batch runs.

Schema and naming conventions:

- Enforce presence of attributes: `xml:lang`, `iso639-3`, `iso15924`, `dir`, `key`, `n` in `<udhr>` root.
- `key` format recommendation: `lang[_script[-variant]]` (lowercase language, titlecase script; hyphen to separate variants if needed).

YAML normalization (merged/):

- Canonical fields: `key`, `language`, `script`, `source`, `article`, `text`, `license`, `provenance`, `updated`.
- Keep large historical variants in `releases/` or tag with `version` field; default `udhr-art1.yaml` stays concise.

## Risks & Mitigations

- Risk: CI timeouts due to many files.
  - Mitigation: shard validation across matrix (e.g., split by first letter of filename).
- Risk: Divergent naming conventions in legacy files.
  - Mitigation: introduce mapping table and non-breaking normalization during merges.
- Risk: Contributor friction from new tooling.
  - Mitigation: keep `requirements.txt` path working; document both `uv` and classic venv.

## Success Criteria

- PRs must pass: XML schema validation, index checks, ruff lint, YAML schema lint.
- Single CLI entrypoint covers existing scripts’ core workflows.
- README gains runnable, copy-paste examples with expected outputs.
- Merged datasets become reproducible from source YAMLs and logs record provenance.

## Next Steps (Suggested PR sequence)

1) Add validation scripts + CI workflow; no data changes.
2) Introduce unified CLI wrapper around existing scripts (non-breaking).
3) Migrate dependencies to uv + ruff; add pre-commit.
4) Update documentation with examples; add CONTRIBUTING.
5) Normalize merged files into canonical + reproduce pipeline.

