# Changelog Reference
> Used by **Component Spec Writer** at Step 3 (component mode).
> Defines required structure for `specs/components/[component-name]/changelog.md`.

## [Objective Name]

- Bullet list of changes.
- Don't list details, only overall changes.
- Keep compact but clear.
- Another entry with same objective name must be appended to current section. Don't create duplicate sections.
- Don't create a new section for same objective. One objective = one section.
- Add entry to current objective section.
- If two entries in same objective conflict, resolve to latest.
- A section can NEVER have conflicting entries. Always review and resolve after adding.

## Shadcn Install Entries

When component is installed from shadcn registry, use `[Shadcn install]` prefix and record source id + local overrides summary:

```
- [Shadcn install] Button: installed shadcn/button; overrides: variant map extended with `destructive-outline`, border-radius token mapped to `--radius-sm`.
```

If no local overrides: `no local overrides`.

Example with no overrides:
```
- [Shadcn install] Label: installed shadcn/label; no local overrides.
```
