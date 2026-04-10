fix this issues.
 
Do not fine tune for examples. fix them logically.

- spec writer should only resolve design values inside the table that are directly controlled by the current component not it's dependency compoents.
for example card background is handled by the card component it should not end up in the value table of a compnent which is using card.