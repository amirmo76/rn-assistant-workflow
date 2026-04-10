implement a python script under scripts folder called `rn-architect.py`
install script must include this as well.

two possible input (with a give yaml file):
    - list all the components in the scope:
        - a list of all unique component in the yaml file.
    - list of all direct dependencies of a component:
        - a list of all unique any component that directly is imported and used by the component.


important notes:
- parantheses add extra context do not change the component.
- every block list all the direct dependencies of the root comopnent. there could be repetitive instances of a single component.
- in the example the only components that have dependencies are the LoginCard and Button
- Card does not have dependency.
- InputGroupInput is a dependency of the LoginCard not the InputGroup. it is merely passed to it as a child.


after writing it fully test it to make sure it works expectedly.

rn-assistant agent the workflow and spec write agents should use this script instead of architect agent now.

assistant will use it to get all the components in the scope.
spec writer:
 - objective mode -> get all the components in the scope: these are the components that need writing/updating or verfying they comply with the objective. never omits any of them.
 - component mode -> gets the direct dependencies meaning the exact components that will be imported and used by that component.

tree.yaml file will still be passed to the spec writer agent for additional context and parsing to see how a dependency is being used. but the source of truth the script answer for dependency list should always make sure a parsed result from the tree does not conflict with the dependency list if so it means it made a wrong conclusion.