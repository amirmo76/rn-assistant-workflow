# Branch A DAG and Tasking Reference
> Used by SDD Task Planner during Step 4.0 and Step 4.1.

## DAG requirements
- Build order must be acyclic.
- Nested component dependencies must appear before dependents.
- plan.json must define batch boundaries for safe parallel execution.

## Minimum plan.json fields
- component
- dependencies
- batch
- target_paths
- spec_path

## tasks.md requirements
- group tasks by execution batch
- each task includes status, owning worker role, retry count, target paths, verification commands, and promotion rules
- each task maps back to one approved spec
- no inferred work outside approved specs

## Batch policy
- Only independent tasks share a batch.
- Future batches remain queued until the current batch passes aggregate verification.