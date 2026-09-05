# Change log

## 2026-09-05: project recovery

- Reconciled the untracked local directory with the existing GitHub history.
- Consolidated the unchanged dataset and model, restored GitHub-only research files, and recovered a deleted intermediate dataset.
- Preserved original notebooks, notes, scripts, and extension prototypes with a file-level recovery manifest.
- Added a working notebook with repository-relative paths and separate generated model output.
- Added repository integrity checks, a model smoke check, and GitHub Actions validation.
- Documented missing source data, persistent streak leakage, and the browser extension integration gaps.
- Set the project priority to the extension and live feature pipeline, with classifier tuning deferred.

The full findings and verification boundaries are in [`docs/recovery-audit.md`](docs/recovery-audit.md).
