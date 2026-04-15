# Changelog Reference
> Used by **Component Spec Writer** at Step 3 (component mode).
> Defines the required structure and rules for `specs/components/[component-name]/changelog.md`.

## [Objective Name]

- Bulletpiont list of changes.
- Do not list details only overall changes.
- Keep it compact but clear.
- Another entry with the same objective name must be appended to the current section. Do not create a duplicate section with the same name and date.
- Do not create a new section for the same objective. One objective will have one section.
- Add the entry to current objective section.
- If two entry in the same objective conflict resolve to the latest.
- An objective section can NEVER have conflicting entries. Always review and resolve after adding.

## Shadcn Install Entries

When a component is installed from the shadcn registry, the changelog entry must use the `[Shadcn install]` prefix and record the source id plus a summary of local overrides:

```
- [Shadcn install] Button: installed shadcn/button; overrides: variant map extended with `destructive-outline`, border-radius token mapped to `--radius-sm`.
```

If there are no local overrides, write: `no local overrides`.

Example with no overrides:
```
- [Shadcn install] Label: installed shadcn/label; no local overrides.
```
