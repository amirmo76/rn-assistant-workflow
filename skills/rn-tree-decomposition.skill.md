# Skill: React Native Component Tree Decomposition

This skill teaches you how to decompose a screen screenshot into a semantic
**dependency tree** — a flat, ordered list of reusable components and their
direct child dependencies — modelled after the shadcn/ui component philosophy
adapted for React Native.

---

## 1. Dependency Tree vs Instance Tree

**Instance tree** (WRONG — mirrors Figma layer structure):
```
Frame_24
  Group_12
    Text_7 "Welcome"
    Frame_8
      InputRow_1
      InputRow_2
```

**Dependency tree** (CORRECT — semantic components with reuse):
```
Card                → CardHeader, CardContent, CardFooter
CardHeader          → CardTitle, CardSubtitle
InputGroup          → Label, Input, Icon
```

The dependency tree answers the question: *"What reusable components does this
component directly compose?"*  Never transcribe Figma layer names. Always
infer semantic names from visual role and intent.

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

Rules:
- `root` is always the screen itself, never a component inside it.
- `components` is a **flat list** — not nested.
- `dependencies` lists names of other components in the same file that this
  component directly renders. Leaf primitives use `[]`.
- `short_description` describes visual role in plain English. No code, no
  style values.
- Every component that appears in any `dependencies` list must also appear
  as its own entry, unless it is an obvious sub-label / inline variant that
  does not warrant a separate reusable entry.
- List order: outer-to-inner, then shared primitives last.

---

## 3. The Five Decomposition Principles

### 3.1 Name by role, not by instance
- Use `Button`, not `LoginButton` or `PrimaryButton`.
- Use `InputGroup`, not `PhoneInputGroup`.
- Use `Card`, not `LoginCard`.
- Treat visual variants (color, size, style) as props, never separate
  components.

### 3.2 Prefer reuse over proliferation
If two or more visual elements share the same structure and purpose, model
them as one component used multiple times with different data. For example,
a phone input field and a password input field are both `InputGroup` — model
`InputGroup` once, not `PhoneInputGroup` + `PasswordInputGroup`.

### 3.3 Split on responsibility boundaries
Split a region into sub-components when:
- It has a distinct, self-contained visual responsibility (header vs content
  vs footer inside a card).
- It is reused elsewhere in the same screen or will likely be reused across
  screens.
- Splitting produces a meaningful, nameable unit.

Do NOT split when:
- The result would be a trivially thin wrapper with no independently useful
  purpose.
- The only reason to split is "it has children in Figma".

### 3.4 Distinguish container from content
A frosted/blurred sheet that wraps a card is NOT the same component as the
card inside it. The outer container handles visual framing; the inner card
handles content. Model them separately. Use `WrapperCard` (or `BottomSheet`)
for the outer container and `Card` for the inner content block.

### 3.5 Preserve the shadcn Card anatomy for RN
Even without a web DOM, React Native cards follow the same logical anatomy:

```
Card
  CardHeader       ← title bar region
    CardTitle      ← main heading text (leaf)
    CardDescription / CardSubtitle  ← supporting text (leaf)
  CardContent      ← main body / form / list area (leaf or composes form items)
  CardFooter       ← bottom action area (leaf or composes buttons)
```

Use these names. Do not invent `CardTop` or `CardBody`.

---

## 4. Primitive Catalogue for React Native

Primitives are leaf components (no child component dependencies). They map
directly to native building blocks. Recognise them in a screenshot and use
the canonical names below.

| Visual element | Canonical name | Notes |
|---|---|---|
| Text input field (box with cursor) | `Input` | Wraps TextInput |
| Label above or alongside an input | `Label` | Plain text in form context |
| Icon (glyph / vector symbol) | `Icon` | Any icon regardless of source |
| Labelled input with icon | `InputGroup` | Composes Label + Input + Icon |
| Tappable button with fill or border | `Button` | No variants in name |
| Inline tappable text / underline | `Link` | Pressable text navigation |
| Image filling the view or a region | `Image` or `BackgroundImage` | `BackgroundImage` when it fills the screen behind content |
| Bottom-anchored screen region | `Footer` | Actions at bottom of screen |
| Checkbox / toggle | `Checkbox` / `Switch` | |
| Badge / chip / tag | `Badge` | |
| Avatar / profile image | `Avatar` | |
| Progress indicator | `ProgressBar` / `Spinner` | |
| Divider / separator | `Separator` | |
| List row / item | `ListItem` | Use `List` as the parent |
| Modal overlay | `Modal` | |
| Top navigation bar | `NavBar` | Header with back/title/actions |
| Bottom tab bar | `TabBar` | |

> **RN vs web compensation**: React Native has no `<a>`, no `<form>`, no
> CSS flexbox inheritance the same way. However component naming for
> semantic purposes follows the same shadcn/radix logic. DO NOT use HTML
> element names (`Div`, `Span`, `Section`). DO use RN-aware slot names.

---

## 5. Container / Wrapper Patterns

### 5.1 Screen with background + overlay card
```
ScreenName (root, type: Screen)
  BackgroundImage        → (no deps) full-screen image
  WrapperCard            → WrapperCardHeader, WrapperCardContent
    WrapperCardHeader    → WrapperCardTitle
      WrapperCardTitle   → (no deps)
    WrapperCardContent   → Card
      Card               → CardHeader, CardContent
        CardHeader       → CardDescription (or CardSubtitle)
        CardContent      → InputGroup, Link (etc.)
```

### 5.2 Form field group
```
InputGroup → Label, Input, Icon
  Label    → (no deps) field label text
  Input    → (no deps) text box
  Icon     → (no deps) leading or trailing icon
```
All three are always separate leaves. Never merge icon into Input.

### 5.3 Footer action bar
```
ScreenFooter             → (no deps, or SignUpPrompt + Button)
  SignUpPrompt           → Link
  Button                 → (no deps)
```
If the footer is very simple (one button + one static text) you may keep it
as a single `Footer` leaf. Only split when the footer contains semantically
distinguishable sub-regions.

### 5.4 Link as a named primitive
`Link` is a primitive leaf (Pressable + Text). When a screen has multiple
distinct link *usages* (e.g., ForgotPassword and SignUp), model one generic
`Link` primitive and use it multiple times. The specific text / destination
is a prop, not a new component.

---

## 6. What NOT to include

- Style info: no colors, font sizes, spacing, border-radius.
- Implementation details: no prop types, hook usage, API calls.
- Figma-specific: no layer IDs, component set names, variant keys.
- Over-split: do not create a component just because Figma has a group.
- Screen-level wrappers: do not add `SafeAreaView` or `ScrollView` at the
  root — those are infrastructure, not semantic components.

---

## 7. Worked Example: Login Screen

Given a screen with: full-screen food photo background, frosted bottom card
with welcome title, white inner card with subtitle, two labeled icon+input
fields, a forgot-password link, a sign-up footer prompt, and a login button.

```json
{
  "root": { "name": "LoginScreen", "type": "Screen" },
  "components": [
    {
      "name": "BackgroundImage",
      "dependencies": [],
      "short_description": "Full-screen background image with a gradient overlay"
    },
    {
      "name": "WrapperCard",
      "dependencies": ["WrapperCardHeader", "WrapperCardContent"],
      "short_description": "Frosted card with a semi-transparent background anchored to the bottom half"
    },
    {
      "name": "WrapperCardHeader",
      "dependencies": ["WrapperCardTitle"],
      "short_description": "Header section of the wrapper card"
    },
    {
      "name": "WrapperCardTitle",
      "dependencies": [],
      "short_description": "Title displayed at the top of the wrapper card"
    },
    {
      "name": "WrapperCardContent",
      "dependencies": ["Card"],
      "short_description": "Main content area of the wrapper card"
    },
    {
      "name": "Card",
      "dependencies": ["CardHeader", "CardContent"],
      "short_description": "White rounded card containing the login form"
    },
    {
      "name": "CardHeader",
      "dependencies": ["CardDescription"],
      "short_description": "Header section of the card with instructional text"
    },
    {
      "name": "CardDescription",
      "dependencies": [],
      "short_description": "Subtitle or instruction text inside the card header"
    },
    {
      "name": "CardContent",
      "dependencies": ["InputGroup", "Link"],
      "short_description": "Main content area of the card containing form fields"
    },
    {
      "name": "InputGroup",
      "dependencies": ["Label", "Input", "Icon"],
      "short_description": "Labelled form field with an icon and text input"
    },
    {
      "name": "Label",
      "dependencies": [],
      "short_description": "Field label text displayed above an input"
    },
    {
      "name": "Input",
      "dependencies": [],
      "short_description": "Text input field"
    },
    {
      "name": "Icon",
      "dependencies": [],
      "short_description": "Icon displayed inside a form field"
    },
    {
      "name": "Link",
      "dependencies": [],
      "short_description": "Tappable inline text used for navigation"
    },
    {
      "name": "Footer",
      "dependencies": ["SignUpPrompt", "Button"],
      "short_description": "Bottom-anchored screen footer with sign-up prompt and login button"
    },
    {
      "name": "SignUpPrompt",
      "dependencies": ["Link"],
      "short_description": "Static text with an inline sign-up link"
    },
    {
      "name": "Button",
      "dependencies": [],
      "short_description": "Primary action button"
    }
  ]
}
```

---

## 8. Checklist Before Writing the Tree

- [ ] Have I named every component by role/intent, not Figma layer name?
- [ ] Does each `InputGroup` (or equivalent) reuse `Input`, `Icon`, `Label`
      as separate primitives rather than being monolithic?
- [ ] Is there at most one `Card` pattern (not `LoginCard`, `SignupCard`)?
- [ ] Are all leaf primitives using canonical names from §4?
- [ ] Does the `Card` anatomy follow §3.5 (CardHeader, CardContent, CardFooter)?
- [ ] Is the outer frosted/blurred wrapper separate from the inner `Card`?
- [ ] Are style/spacing details absent from the output?
- [ ] Does every name in any `dependencies` array have its own entry in
      `components`?
- [ ] Is the `root` the screen, not a sub-component?
