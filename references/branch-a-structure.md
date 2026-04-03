# Branch A Structure Reference
> Used by SDD Mapper and SDD Extractor during Step 2.0 and Step 2.1.

## Page tree requirements
- Root must correspond to the validated structural container.
- Preserve stable identifiers, normalized names, sibling order, and parent references.
- Keep the artifact deterministic so repeated runs produce stable output ordering.

## Extraction requirements
- One component JSON per mapped component node.
- Include raw layout, visual, and text properties.
- Include provenance fields: node_id, target tree path, extraction timestamp, target name.
- Do not tokenize or synthesize styles during extraction.

## Naming policy
- Page artifact: .ui-state/pages/[target-name]-tree.json
- Screenshot artifact: .ui-state/pages/[target-name]-reference.png
- Component artifacts: .ui-state/components/[ComponentName].json