I want to add the Execution step to the workflow. update the workflow, assistant and any other agents to comply with this rules.

- we move directly from planning to exec.
- no more tasking and tasker agent.
- orchestrator will spawn workers according to the plan execution map. (respecting parallel and sequential work)
- after each phase is done a verfication prompt will be asked using `vscode/askQuestions` from the user.
- if user verfies moves to the next phase.
- if user ask for change -> apply change (loop until explicit approval.)
- a worker will execute works under one component.
- orchestrator will spawn a worker per component works in each phase in parallel.
- an orchestrator will approach phase by phase spawning needed workers in parallel.
- a worker will run typecheck/lint/test making sure everything related to its work is ok before reporting done.
