# Update

Update the workflow and the required agent/reference files to support these requirements.

Update smart so everything is clear, do not spam rules.

## Requirement 1: RN Assistant Must Never Stop Early

RN Assistant should never terminate mid-workflow. All approvals and questions must go through `vscode/askQuestions`. Only after final approval of the last step will it terminate.

Current problem: it stopped mid-flow and asked for approval using plain text instead of `vscode/askQuestions`. The workflow must keep flowing continuously — no breaks, no plain-text approval requests.

## Requirement 2: RN Architect Must Resolve All Required Component Architectures

Update the RN Architect agent, the `rn-tree-decomposition` skill, and the workflow to support the following behavior.

**Do not fine-tune for this example. Use it to understand the intent only.**

Example — Objective: implement a `LoginCard` component that accepts a username and password and submits.

Proposed architecture (by the user):
`LoginCard -> Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter, Button, Field, Input, Label`

Intended tree structure (not an implementation — just to communicate the shape):

```jsx
<Card>
  <CardHeader>
    <CardTitle />
    <CardDescription />
  </CardHeader>
  <CardContent>
    <Field>
      <Label />
      <Input />
    </Field>
    <Field>
      <Label />
      <Input />
    </Field>
  </CardContent>
  <CardFooter>
    <Button />
  </CardFooter>
</Card>
```

RN Architect must understand which components the objective depends on and clarify the full dependency tree through discussion — not write implementations or specs. The output architecture must be explicit: the graph, the atomic levels, and the complete dependency list.

The architecture follows atomic design. Every component must be broken down until all leaves are atoms. If any component in the tree is a molecule or above, its internal structure must also be defined — recursively — until every branch terminates at atoms. No molecule, organism, or template may remain opaque.

When a required component's architecture is unclear or does not yet exist, RN Architect must ask and discuss through `vscode/askQuestions` until that component's architecture is finalized and approved — exactly as it does for the objective itself. This repeats for every non-atom component in the tree until all architectures, at every level, are approved.

**A component spec must include an explicit, complete list of its direct dependencies.**

**If a dependency itself does not have an explicit architecture, it must be finalized before the parent is considered done.**

**An objective spec is not ready until every dependent component spec is fully ready.**

## Requirement 3: Reference Files Must Declare Their Consumers

All reference files should include a usage header at the top declaring which agent uses them and at which step:

```markdown
# Reference Title
> Used by [Agent Name] at Step N [and by [Agent Name] at Step N].
> Defines [what it defines].
```

Adjust the wording to the current workflow agents and step numbers. Do not copy this example literally.

## Requirement 4: Agents Must Load Their Reference as Step 0

Any agent that has a defined process and depends on a reference file must load and read that reference as its first step (step 0) before doing anything else.
