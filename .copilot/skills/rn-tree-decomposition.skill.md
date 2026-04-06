# Skill: React Native Component Tree Decomposition

This skill teaches you how to decompose a screen screenshot into a semantic **dependency tree** — a flat, ordered list of reusable components and their direct child dependencies — modelled after the shadcn/ui component philosophy adapted for React Native.

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

The dependency tree answers the question: *"What reusable components does this component directly compose?"* Never transcribe Figma layer names. Always infer semantic names from their visual role and intent.

---

## 2. Output Format

```json
{
  "root": { "name": "ScreenName", "type": "Screen" },
  "components": [
    {
      "name": "ComponentName",
      "dependencies": ["Child1", "Child2"],
      "short_description": "one-line visual role description"
    }
  ]
}
```

**Rules:**
* `root` is always the screen itself, never a component inside it.
* `components` is a **flat list**, not nested.
* `dependencies` lists the names of other components in the same file that this component directly renders. Leaf primitives MUST explicitly use an empty array `[]`.
* `short_description` describes the visual role in plain English. No code, no style values.
* Every component that appears in any `dependencies` list must also appear as its own standalone entry in the `components` array, unless it is a trivial inline variant.
* List order: outer-to-inner, concluding with shared primitives.

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

## 5. Container / Wrapper Patterns

### 5.1 Screen with background + overlay card
```text
ScreenName (root, type: Screen)
  BackgroundImage        → [] (full-screen image)
  WrapperCard            → WrapperCardHeader, WrapperCardContent
    WrapperCardHeader    → WrapperCardTitle
      WrapperCardTitle   → []
    WrapperCardContent   → Card
      Card               → CardHeader, CardContent
        CardHeader       → CardDescription
        CardContent      → InputGroup, Link
```

### 5.2 Form field group
```text
InputGroup → Label, Input, Icon
  Label    → [] (field label text)
  Input    → [] (text box)
  Icon     → [] (leading or trailing icon)
```
All three are always separate leaves. Never merge the icon into the `Input` primitive.

### 5.3 Footer action bar
```text
ScreenFooter             → SignUpPrompt, Button
  SignUpPrompt           → Link
  Button                 → []
```
If the footer is extremely simple (one button + one static text), you may keep it as a single `Footer` leaf. Only split when the footer contains semantically distinguishable sub-regions.

### 5.4 Link as a named primitive
`Link` is a primitive leaf (Pressable + Text). When a screen has multiple distinct link *usages* (e.g., "Forgot Password" and "Sign Up"), model one generic `Link` primitive and use it multiple times. The specific text or destination is a prop, not a new component.

---

## 6. What NOT to Include

* **Style details:** No colors, font sizes, spacing, or border-radii.
* **Implementation logic:** No prop types, hook usage, or API calls.
* **Figma artifacts:** No layer IDs, component set names, or variant keys.
* **Over-splitting:** Do not create a component purely because a bounding box exists in the design file.
* **Infrastructure wrappers:** Do not add `SafeAreaView`, `ScrollView`, or `KeyboardAvoidingView` to the tree. These are structural React Native implementations, not semantic UI components.

---

## 7. Quality Checklist

* [ ] Have I named every component by role/intent rather than Figma layer name?
* [ ] Does each `InputGroup` reuse `Input`, `Icon`, and `Label` as separate primitives rather than being monolithic?
* [ ] Are all leaf primitives utilizing the canonical names from Section 4?
* [ ] Does the `Card` anatomy strictly follow Section 3.4 (`CardHeader`, `CardContent`, `CardFooter`)?
* [ ] Are all styling and spatial details completely absent from the output?
* [ ] Does every component listed in a `dependencies` array have its own standalone entry in the `components` array?
* [ ] Is the `root` strictly defined as the screen itself, rather than a sub-component?