# Skill: React Native Component Architecture Decomposition

This skill teaches you how to architect a single React Native component: how to assign its atomic design level and decide what direct children it should compose. It is modelled after the shadcn/ui component philosophy adapted for React Native.

**Scope:** You work on one component at a time. Your goal is to define its immediate children only — not the full subtree. You may name or briefly describe deeper descendants only when they belong to a tightly coupled organism (e.g. a Card's mandatory slot anatomy), but you do not design them here.

---

## 1. Dependency Tree vs. Instance Tree

**Instance tree** (WRONG — mirrors Figma layer structure):
```text
Frame_24
  Group_12
    Text_7 "Welcome"
    Frame_8
      InputRow_1
      InputRow_2
```

**Dependency tree** (CORRECT — semantic components with reuse):
```text
Card         → CardHeader, CardContent, CardFooter
CardHeader   → CardTitle, CardSubtitle
InputGroup   → Label, Input, Icon
```

The dependency tree answers: *"What reusable components does this component directly compose?"* Never transcribe Figma layer names. Always infer semantic names from their visual role and intent.

---

## 2. Output Format

The finalized architecture for a single component is expressed as:

**Atomic design level** — one of: `atom`, `molecule`, `organism`, `template`, `page`.

**Dependency graph** — arrow notation listing this component and its direct children. Leaf components (no children of their own) appear on their own line with no arrow.

```
ComponentName -> ChildA, ChildB, ChildC
ChildA
ChildB -> LeafX, LeafY
ChildC
LeafX
LeafY
```

**Rules:**
* The subject component is listed first.
* Children are listed in visual order: top-to-bottom, left-to-right.
* Leaf children appear as separate lines with no `->`.
* No style data, no Figma metadata, no implementation details.
* Only include children one level deep. Do not recurse further unless a tightly coupled organism mandates it (e.g. Card slot anatomy per §3.4).

### 2.1 Atomic Design Levels

| Level | Assign when… |
| :--- | :--- |
| `atom` | The component has no child components — it is a single primitive (Button, Icon, Label, Input). |
| `molecule` | The component composes 2–4 atoms into one focused unit (InputGroup, ListItem, Badge). |
| `organism` | The component composes multiple molecules or atoms into a distinct section of the UI (Card, NavBar, FormSection). |
| `template` | The component defines a page-level layout skeleton with named regions, no data. |
| `page` | The component is a screen rendered by a navigator; it provides all data and orchestrates the layout. |

---

## 3. The Four Decomposition Principles

### 3.1 Name by role, not by instance
* Use `Button`, not `LoginButton` or `PrimaryButton`.
* Use `InputGroup`, not `PhoneInputGroup`.
* Treat visual variants (color, size, style) as props, never as separate components.

### 3.2 Prefer reuse over proliferation
If two or more visual elements share the same structure and purpose, model them as one component used multiple times with different data. For example, a phone input field and a password input field are both `InputGroup`. Model `InputGroup` once; do not create `PhoneInputGroup` and `PasswordInputGroup`.

### 3.3 Split on responsibility boundaries
Split a region into sub-components when:
* It has a distinct, self-contained visual responsibility (e.g., header vs. content vs. footer inside a card).
* It is reused elsewhere in the same screen or will likely be reused across screens.
* Splitting produces a meaningful, nameable unit.

**Do NOT split when:**
* The result would be a trivially thin wrapper with no independently useful purpose.
* The only reason to split is because "it has children in Figma."

### 3.4 Preserve the shadcn style anatomy for RN
Even without a web DOM, React Native cards follow the same logical anatomy:

```text
Card
  CardHeader                    ← title bar region
    CardTitle                   ← main heading text (leaf)
    CardDescription / CardSubtitle ← supporting text (leaf)
  CardContent                   ← main body / form / list area
  CardFooter                    ← bottom action area
```

Use these exact names. Do not invent custom slots like `CardTop` or `CardBody`.

---

## 4. Primitive Catalogue for React Native

Primitives are leaf components (no child component dependencies). They map directly to native building blocks. Recognize them in a screenshot and use the canonical names below.

| Visual element | Canonical name | Notes |
| :--- | :--- | :--- |
| Text input field (box with cursor) | `Input` | Wraps TextInput |
| Label above or alongside an input | `Label` | Plain text in form context |
| Icon (glyph / vector symbol) | `Icon` | Any icon regardless of source |
| Labelled input with icon | `InputGroup` | Composes Label + Input + Icon |
| Tappable button with fill or border| `Button` | No variants in name |
| Inline tappable text / underline | `Link` | Pressable text navigation |
| Image filling a view or region | `Image` or `BackgroundImage` | Use `BackgroundImage` for full-screen backdrops |
| Bottom-anchored screen region | `Footer` | Actions at bottom of screen |
| Checkbox / toggle | `Checkbox` / `Switch` | |
| Badge / chip / tag | `Badge` | |
| Avatar / profile image | `Avatar` | |
| Progress indicator | `ProgressBar` / `Spinner`| |
| Divider / separator | `Separator` | |
| List row / item | `ListItem` | Use `List` as the parent |
| Modal overlay | `Modal` | |
| Top navigation bar | `NavBar` | Header with back/title/actions |
| Bottom tab bar | `TabBar` | |

> **RN vs. Web Compensation:** React Native has no `<a>`, no `<form>`, and no CSS flexbox inheritance in the same way the web does. However, component naming for semantic purposes follows the exact same shadcn/radix logic. **DO NOT** use HTML element names (`Div`, `Span`, `Section`). **DO** use RN-aware slot names.

---

## 5. Example Patterns

These are examples of common component architectures. Apply the same thinking to the component you are currently working on.

### 5.1 Card organism
```text
Card -> CardHeader, CardContent, CardFooter
CardHeader -> CardTitle, CardSubtitle
CardTitle
CardSubtitle
CardContent -> InputGroup, Link
CardFooter -> Button
```
The three slots (Header/Content/Footer) are always present per §3.4. Do not invent custom slot names like `CardTop` or `CardBody`.

### 5.2 Form field group
```text
InputGroup -> Label, Input, Icon
Label
Input
Icon
```
All three are always separate leaves. Never merge the icon into the `Input` primitive.

### 5.3 Footer action bar
```text
Footer -> SignUpPrompt, Button
SignUpPrompt -> Link
Link
Button
```
If the footer is extremely simple (one button + one static text), you may keep it as a single `Footer` leaf. Only split when the footer contains semantically distinguishable sub-regions.

### 5.4 Link as a named primitive
`Link` is a primitive leaf (Pressable + Text). When a component has multiple distinct link *usages* (e.g., "Forgot Password" and "Sign Up"), model one generic `Link` primitive. The specific text or destination is a prop, not a new component.

---

## 6. What NOT to Include

* **Style details:** No colors, font sizes, spacing, or border-radii.
* **Implementation logic:** No prop types, hook usage, or API calls.
* **Figma artifacts:** No layer IDs, component set names, or variant keys.
* **Over-splitting:** Do not create a component purely because a bounding box exists in the design file.
* **Infrastructure wrappers:** Do not add `SafeAreaView`, `ScrollView`, or `KeyboardAvoidingView` to the tree. These are structural React Native implementations, not semantic UI components.
* **Deep subtrees:** Do not recursively design children-of-children unless they are a tightly coupled organism. Each component's internals are designed in a separate architecture session.

---

## 7. Quality Checklist

* [ ] Have I named every component by role/intent rather than Figma layer name?
* [ ] Does each `InputGroup` reuse `Input`, `Icon`, and `Label` as separate primitives rather than being monolithic?
* [ ] Are all leaf primitives utilizing the canonical names from Section 4?
* [ ] Does the `Card` anatomy strictly follow Section 3.4 (`CardHeader`, `CardContent`, `CardFooter`)?
* [ ] Are all styling and spatial details completely absent from the output?
* [ ] Does every component listed in the dependency graph appear as its own line with its own children (or as a leaf)?
* [ ] Is the atomic design level correctly assigned for the subject component itself (not its children)?
* [ ] Have I stayed at one level of depth — direct children only — unless a tightly coupled organism (e.g. Card anatomy) requires naming one level deeper?