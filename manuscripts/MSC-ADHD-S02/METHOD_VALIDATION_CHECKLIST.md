# S02 method-validation checklist

- [x] Machine-readable recovery-event schema exists.
- [x] Semantic validator exists.
- [x] Deterministic controller replay exists.
- [x] Unit tests cover recovery-event semantics.
- [x] Telemetry queue contract and tests exist.
- [x] Pin the manuscript's descriptive schema snapshot: v0.6.0, Git blob `0a7ee0a3c7e8db771d64c2aa188692fbe0f6c751`. This is not a participant-protocol or export freeze.
- [x] Declare the conformance corpus: three reference events and seven deterministic negative mutations in `conformance/manifest.yaml` and the generator. Test execution remains open.
- [x] Commit the schema-derived field table (`tables/schema_fields.tex`); drift check must still run on the submission SHA.
- [x] Add source-level regression assertions for each negative mutation's diagnostic location and reason (`tests/test_s02_conformance_diagnostics.py`); execution remains open.
- [ ] Run and archive the recovery-event validator regressions (including non-finite input rejection), conformance generator's JSON/CSV, diagnostic-specificity test, replay and queue tests at the exact source SHA. Record failures and environment; do not substitute source inspection for PASS.
- [ ] Verify that generated test-result artifacts are reproducible from an authorized execution; do not manually quote unexecuted counts.
- [ ] Add a minimal independent implementation/replay example if feasible.
- [ ] Complete literature positioning against serious-game telemetry standards.
- [ ] Freeze manuscript claims in research/claim_ledger.yaml.
- [ ] Reverify target journal and article type before submission.

## Reproduction commands (repository root)

```bash
python -m unittest discover -s tests -p 'test_recovery_event_validator.py'
python -m unittest discover -s tests -p 'test_s02_schema_table.py'
python -m unittest discover -s tests -p 'test_s02_conformance_diagnostics.py'
python -m unittest discover -s tests -p 'test_controller_replay.py'
python -m unittest discover -s tests -p 'test_telemetry_queue.py'
python scripts/generate_s02_schema_table.py --check
python scripts/generate_s02_conformance_report.py --output artifacts/s02-conformance
```

## Exact-revision evidence capture (authorized isolated checkout)

Execute from a clean checkout of the PR head in an isolated, nonpersistent environment. Do not run feature-branch code on the permanent Actions runner. Record the resolved commit, Python and LaTeX tool versions, command exit statuses, and unedited stdout/stderr. For the complete suite, use `python -m unittest discover -s tests -p 'test_*.py'` in addition to the focused commands above. For S02 PDF, use the repository's documented latexmk/Biber build command and retain its build log; do not infer success from a generated filename alone.

After the commands complete, compute SHA-256 digests of the conformance JSON/CSV, schema-derived table, test logs and PDF (when produced). Record the exact source commit, schema blob `0a7ee0a3c7e8db771d64c2aa188692fbe0f6c751`, runtime versions, exit codes, artifact paths and digests together in the PR. Compare a second independently generated set of conformance artifacts against the first, ignoring only explicitly documented nondeterministic metadata. Any missing file, failed command, changed schema blob, mismatch or unavailable tool is FAIL, BLOCKED or NOT_RUN as appropriate, never PASS.

The three reference fixtures and seven negative mutations are a declared synthetic corpus, not a measured performance result. Keep their counts distinct from executed pass/fail totals, and do not use a passing software suite as evidence of construct validity or clinical benefit.

Execution status for this checklist revision: **NOT_RUN** (GitHub connector does not execute private-branch Python or LaTeX). The listed commands are not evidence of passing tests. Archive logs, JSON/CSV, Python version and exact tested SHA before updating the manuscript's results or submission readiness. The regression test command above is required even though PR #89 was merged on 2026-11-07; merging does not establish execution at the merged SHA. PDF compilation, source verification, independent review and journal eligibility remain separate gates.

## Evidence acceptance matrix (execution gate)

| Claim or artifact | Required evidence | Failure condition | Current state |
| --- | --- | --- | --- |
| Pinned structural inventory | Schema blob matches the cited v0.6.0 blob and generated table passes `--check` on the same SHA | Changed blob, table drift or missing log | NOT_RUN |
| Positive and negative conformance | Generator outputs JSON/CSV; all three declared reference cases and seven declared mutations are evaluated with diagnostic-location assertions | Any unexpected acceptance/rejection, missing artifact or diagnostic mismatch | NOT_RUN |
| Replay determinism | Controller replay tests run twice from the same SHA, configuration and runtime; compare normalized outputs | Different semantic outputs or unreported nondeterminism | NOT_RUN |
| Queue semantics | Telemetry queue tests and recovery-event validator regressions pass with raw logs | Missing, reordered or silently reclassified events | NOT_RUN |
| Reproducible package | SHA-256 hashes, runtime versions, exact command exit codes and artifact manifest are retained | Missing provenance, nonzero exit status or unaccounted artifact difference | NOT_RUN |
| Manuscript PDF and references | latexmk/Biber log, bibliography verification and PDF digest correspond to the tested source revision | Build failure, unresolved citation or untraceable PDF | NOT_RUN |

**Interpretation rule:** these are software-conformance gates only. They cannot establish recovery construct validity, transfer, diagnostic accuracy or clinical efficacy. A checklist entry may change to PASS only after the corresponding archived execution evidence is inspected. The manuscript's descriptive schema snapshot does not freeze the participant-facing protocol.

## Independent evidence review protocol

Before marking any gate PASS, a reviewer who did not generate the artifacts must compare the declared conformance manifest with the archived machine-readable outputs. For each positive fixture, record its identifier, observed validator verdict and whether required fields and event ordering satisfy the pinned schema. For each negative mutation, record its identifier, expected diagnostic location/reason, observed diagnostic location/reason and whether rejection occurred for the intended reason. A rejection caused by an unrelated parsing error is not a successful semantic conformance check. Preserve all mismatches, including failures of the validation harness itself.

For replay, compare canonicalized semantic event sequences from two clean runs at the same revision and configuration, retaining original raw outputs as well. Canonicalization may remove only documented volatile metadata; it must not reorder events, discard missing values or normalize away changes in censoring, invalidity, timestamps used for decisions or controller state transitions. Report the exact comparison rule and any differences. If the replay test does not exercise an independently implemented consumer, label the claim **within-implementation determinism**, not cross-implementation interoperability.

The evidence manifest must distinguish **declared fixtures**, **executed test cases**, **passed cases** and **excluded or inconclusive cases**, with explicit denominators. A missing log or absent execution is NOT_RUN, not a zero-failure result. Independent review, journal scope verification and manuscript citation checks remain open until supported by dated evidence.

## Machine-readable evidence record contract (proposed, not executed)

For each command, retain one immutable record with `source_sha`, `schema_blob_sha`, `command`, `working_directory`, `runtime_versions`, `started_utc`, `exit_code`, `stdout_sha256`, `stderr_sha256`, `output_artifacts` (path and SHA-256), and `status`. The `source_sha` must equal the PR head used for the complete run; a new documentation commit invalidates any claim that an earlier SHA is the tested submission revision. Record the operating system, locale, timezone and dependency-lock identifier when relevant. Keep raw logs outside Git if they contain sensitive information; store only non-sensitive checksums and authorized references in the PR.

Use only `PASS`, `FAIL`, `NOT_RUN`, `BLOCKED_TOOL_UNAVAILABLE`, `BLOCKED_PERMISSION` or `INCONCLUSIVE` for individual execution records. `PASS` requires a zero exit code and verified expected outputs, not merely successful process termination. `INCONCLUSIVE` covers a completed run whose diagnostic or comparator is insufficient to adjudicate the claim. A blocked command must include the unavailable capability or denied permission, not a fabricated exit code. An overall gate passes only when every required constituent record passes and the independent reviewer signs off on the evidence mapping.

Before running the corpus, freeze a machine-readable mapping from each fixture/mutation ID to its expected acceptance verdict, diagnostic JSON path and semantic reason. The reviewer must compare observed diagnostics to this mapping without changing expectations after observing outcomes. Any subsequent correction requires a versioned deviation and a fresh run; the synthetic fixtures must not be presented as external validation data.
