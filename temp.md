Let's change some things:

The UI Spec writer agent writes the spec for a component according to the `component-spec.md` reference.

input:
- component name
- context:
    - atomic level of the component.
    - architecture of the component.
    - a visual context (optional) but when provided should have high value. image files or figma urls which using `figma/get_design_context` and `figma/get_screenshot` should be used.

output:
    the newly created or updated spec file for the component now sitting under
    `specs/component-[name]/spec.md`

additional notes:
- it should use the exploer and research agents for things like:
    - already existing spec or implementation.
    - project infra, design system and etc.
    - best practices for a component like this.
    - should it use any library for a feature? how does the industry do it?
    - iteratively discuss with user and ask for verification before considering the spec done.
    - when asking user for verification what it has changed should already be inside the file, so user can see and review change if he wants and verify or provide feedback.


we need another agent as well. called `UI Assistant`:
this agent acts as the orchestrator. knows the overal UI task needed to be done.
it should have a proper workflow.
for example when asked to build or update a component:
 - it should collect the required context. information and visuals if the user have not provided iteratively using `vscode/askQuestions`.
 - using the `explorer` sub agent check the current state.
 - if needed using ui architect builds the architecture for the component. (needs to provide the proper input context to it)
 - uses the `spec writer` sub agent with the proper input to produce/update the proper spec for the component.

and any other required considerations.

keep the workflow as a seperate file under workfows directory. the agent will use this workflow. so in the future we can just update the workflow.