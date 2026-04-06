# Branch A Diffing Reference
> Used by SDD Design Guardian during Step 3.0.

## Diff statuses
- NEW: component does not exist in prior design-state history
- NEW_VARIANT: component family exists but the incoming artifact is a distinct approved variant
- MODIFIED_BASE: existing component base changed materially
- UNCHANGED: no actionable delta
- CONFLICT: incoming artifact collides with existing history and cannot be resolved safely

## Action rules
- Generate specs only for NEW, NEW_VARIANT, and MODIFIED_BASE.
- Exclude UNCHANGED items from spec generation.
- Halt on unresolved CONFLICT items.

## Minimum diff item shape
```json
{
  "component": "Button",
  "status": "MODIFIED_BASE",
  "source_json": ".ui-state/components/Button.json",
  "target_paths": ["src/components/Button.tsx"],
  "spec_path": "specs/queue/Button/spec.md"
}
```