# Update

Update the workflow and the required agent/reference files to support these requirements.

Update smart so everything is clear.

## Changed the architect approach

The architect agent now gets a YAML file and a question and answers that question about the architecture.

When a new objective is created, the assistant will:

1. Create an empty `specs/queue/[name]/tree.yaml` file.
2. Ask the user via `vscode/askQuestions` to fill it with all the architectural changes scoped to the objective.
3. Wait for the user to confirm the file is filled.
4. For each component in the tree, run `RN Architect` with the filled YAML and the question: "What are the direct dependencies of [component]?" to get its exact dependency list.
5. For each component in the tree, spawn `RN Component Spec Writer` — passing the component name, its dependency list from the architect, and the full tree.yaml as context — to create or update its component spec. The spec writer reports what changed.
6. Collect all component spec change reports, then spawn `RN Component Spec Writer` in objective mode — passing the full list of component changes as context — to create the objective spec.

The objective spec will include a list of all affected components and a brief about the creation or update of each.
