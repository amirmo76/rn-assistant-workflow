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

## MCP `get_design_context` compatibility
- The Figma MCP `get_design_context` may return generated code (React/HTML) and a reference screenshot instead of raw node JSON.
- When raw node JSON is not available, the mapper and extractor are allowed to parse the returned code to recover structural information using `data-node-id` attributes and element nesting as a deterministic fallback.
- The extractor must still produce component JSONs that include the required provenance fields. When parsing code, preserve any node ids found in `data-node-id` attributes as `node_id` provenance.
- Prefer using the MCP screenshot returned by `get_design_context` as the canonical reference screenshot stored at `.ui-state/pages/[target-name]-reference.png`.

## Naming policy
- Page artifact: .ui-state/pages/[target-name]-tree.json
- Screenshot artifact: .ui-state/pages/[target-name]-reference.png
- Component artifacts: .ui-state/components/[ComponentName].json