Update the workflow and agents with the following requirements:

1. Initializer
    - Verify that `test`, `lint`, and `typecheck` scripts exist in `package.json` and run successfully.
    - If any required script is missing or broken, add or fix it and re-run until it passes.
    - Keep the existing responsibilities for testing, Storybook, and baseline project readiness.

2. Worker
    - After completing any task, run verification in this order:
      1. type errors
      2. lint errors
      3. test errors
    - Keep iterating until all verification checks pass.
    - Treat "all" as all failures introduced by, or directly related to, the task and its normal verification commands, not unrelated repo-wide issues outside the task scope.

3. Spec directory moves
    - When moving a spec from `queue` to `doing` or from `doing` to `done`, move the entire component directory recursively.
    - Do not copy individual files one by one.
    - Do not leave empty source directories behind.

4. Storybook stories
    - Every story file should include clear documentation or descriptive metadata for the component.
    - Props must be typed, and the story should expose controls for the props that are meaningful to edit and verify.
    - Include stories for the default state, meaningful variants, and any important user-facing states or interaction states.
    - When relevant, add stories for loading, disabled, error, empty, and accessibility-related states.
    - If a component has a user story or usage pattern, include a story that demonstrates it.

5. Component state
    - Prefer controlled components over internal state.
    - Avoid local state unless it is explicitly required by the design or implementation.
    - If local state is necessary, keep it minimal and document why it exists.