# Advanced Unattended Maintenance Plan

## Workflow Contract

- This file is the live queue for the repository's `batch-maintainer` lane.
- Refresh the plan before coding if marker discovery or repository drift shows it is stale.
- Implement approved and unblocked items only.
- Stop on unresolved clarification / decision work, unsafe repository state, failed PR isolation, or validation failures you cannot repair confidently in the current item.

## Last Refresh

- Date: 2026-04-30
- Trigger: bootstrap the maintenance lane because the plan and maintenance prompt files were missing from the repository.
- Marker scan result: no tracked `TODO:`, `ARCH:`, `DESIGN:`, `FIXME:`, or `HACK:` markers were found during this refresh.
- Isolation note: run this workflow on the active PR / remote branch rather than assuming local branch management.

## Approved Queue

| ID | Status | Area | Summary | Validation | Notes |
|----|--------|------|---------|------------|-------|
| M-001 | done | `.github/` | Bootstrap the advanced unattended maintenance workflow assets and sync related instructions. | Existing notebook-output check and file review | Completed on 2026-04-30. |

## Blocked Or Decision Items

- None currently recorded.

## Next Refresh Rule

If the queue is empty, the next unattended maintenance run must refresh this plan before adding new work.
