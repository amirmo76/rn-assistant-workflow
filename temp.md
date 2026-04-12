I need you to improve the planning agent and refernce.
right now it does not seem explicit and clear enogh.
the goal is:
- planner should undrestand what are the components in the scope.
- what is the order? bottom-to-top approach
- what has changed in each component? is it created entirely? some update? using the changelog.
- what are the components that are not dependent on each other?
- group the component works into phases in a format which is absolutly clear which phase is parallel to which phase and which phase is sequential compared to another. the format should have a clear overview so another agent can easily spawn workers in parallel on parallel phases and wait for needed phases to be done to spawn for another dependent one/group of parallel phases. A tree like map of pahases. and then a detailed enogh phase explanation for each.
- Everyone should be able to easily figure out the map of how to do the phases.
- It should heavily focus on how to create a plan which has the right amount of phases. not too much and not too little. just the right amount with a clear map of how to finish all the phases in the quickest way possible by utilizing parallel spawning.
- It should not force parallel when not sure about the dependency of something. It should be safe.