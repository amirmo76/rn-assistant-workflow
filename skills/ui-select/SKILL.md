---
name: ui-select
description: How should a select component be implemented.
---

# What is a select component?

Displays a list of options for the user to pick from—triggered by a button.

## Composition

```
Select
├── SelectTrigger
│   └── SelectValue
└── SelectContent
    ├── SelectGroup
    │   ├── SelectLabel
    │   ├── SelectItem
    │   └── SelectItem
    ├── SelectSeparator
    └── SelectGroup
        ├── SelectLabel
        ├── SelectItem
        └── SelectItem
```

## Components

- `Select`: The root component that manages the state and behavior of the select.
- `SelectTrigger`: The button that the user clicks to open the select dropdown.
- `SelectContent`: The container for the dropdown options.
- `SelectItem`: Represents an individual option in the dropdown.
- `SelectValue`: Displays the currently selected value in the trigger.
- `SelectGroup`: Optional component to group related options together.
- `SelectLabel`: Optional component to label groups of options.

## Example Usage

```jsx
<Select>
  <SelectTrigger className="w-full max-w-48">
    <SelectValue placeholder="Select a fruit" />
  </SelectTrigger>
  <SelectContent>
    <SelectGroup>
      <SelectLabel>Fruits</SelectLabel>
      <SelectItem value="apple">Apple</SelectItem>
      <SelectItem value="banana">Banana</SelectItem>
      <SelectItem value="blueberry">Blueberry</SelectItem>
      <SelectItem value="grapes">Grapes</SelectItem>
      <SelectItem value="pineapple">Pineapple</SelectItem>
    </SelectGroup>
  </SelectContent>
</Select>
```