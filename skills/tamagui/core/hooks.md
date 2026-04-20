# Hooks — useMedia, useTheme, Theme

## useMedia

Responsive breakpoint hook. Tracks which keys are accessed and only re-renders when those change.

```tsx
import { useMedia } from 'tamagui'

function Component() {
  const media = useMedia()

  return (
    <View
      bg={media.sm ? 'red' : 'blue'}
      {...(media.lg && { x: 10, y: 10 })}
    />
  )
}
```

### Inline media props (preferred)

```tsx
<XStack
  bg="red"
  $gtSm={{ bg: 'blue' }}
  $gtMd={{ bg: x > 0.5 ? 'green' : 'yellow' }}
>
  <Button>Hello</Button>
</XStack>
```

When all usages are extractable, the compiler removes the hook and outputs pure CSS.

**Limitations:**
- The proxy object is not iterable — no `Object.keys()` or `in`.
- Use `const media = useMedia()` then `media.sm` (no renaming).

---

## useTheme

Access current theme values. Returns a proxied theme with `Variable` objects.

```tsx
import { useTheme } from 'tamagui'

function Component() {
  const theme = useTheme()

  // On web → CSS var: var(--background). On native → raw value: #fff
  const bg = theme.background.get()

  // Always raw value:
  const bgValue = theme.background.val

  return <ExternalComponent style={{ backgroundColor: bg }} />
}
```

### get() vs .val

| Method | Web | Native |
|--------|-----|--------|
| `.get()` | CSS variable (avoids re-render) | Raw value |
| `.val` | Raw value (causes re-render on change) | Raw value |

With `fastSchemeChange` enabled, `.get()` returns `DynamicColorIOS` on iOS avoiding re-renders too.

### Theme-aware hook

```tsx
function MyComponent(props) {
  // Resolves dark → dark_green → dark_green_MyComponent
  const theme = useTheme(props.theme, 'MyComponent')
}
```

### Compile-time extraction

Both hooks work with the compiler:

```tsx
function App() {
  const theme = useTheme()
  const media = useMedia()

  return (
    <YStack
      y={media.sm ? 10 : 0}
      bg={media.lg ? theme.red : theme.blue}
    />
  )
}
// Compiles to pure CSS + className on web
```

---

## Theme Component

Change themes anywhere in the tree:

```tsx
import { Theme, Button } from 'tamagui'

<Theme name="dark">
  <Button>Dark button</Button>
  <Theme name="pink">
    <Button>dark_pink theme</Button>
  </Theme>
</Theme>
```

Sub-themes are auto-resolved: inside `<Theme name="dark">`, using `<Theme name="pink">` resolves to `dark_pink`.

### Theme prop on components

```tsx
<Button theme="blue">Blue button</Button>
<Card theme="purple">Purple card</Card>
```

### Theme tokens in styles

```tsx
// Access theme values with $ prefix
<View bg="$background" color="$color" borderColor="$borderColor" />
<Text color="$color12" />

const Styled = styled(View, { bg: '$background' })
```

---

## createStyledContext

Share values between parent and child styled components:

```tsx
import { createStyledContext, styled, View, Text } from 'tamagui'

const ButtonContext = createStyledContext({ size: '$md' as SizeTokens })

const ButtonFrame = styled(View, {
  context: ButtonContext,
  variants: {
    size: { '...size': (val, { tokens }) => ({ p: tokens.size[val] }) },
  } as const,
})

const ButtonText = styled(Text, {
  context: ButtonContext,
  variants: {
    size: { '...size': (val, { font }) => ({ fontSize: font?.size[val] }) },
  } as const,
})

// Parent passes size down to children via context automatically
const Button = ButtonFrame.styleable((props, ref) => (
  <ButtonFrame ref={ref} {...props}>
    <ButtonText>{props.children}</ButtonText>
  </ButtonFrame>
))

// Usage — size flows to both frame and text
<Button size="$lg">Hello</Button>
```

---

## getTokens / getVariable

```tsx
import { getTokens, getVariable, getVariableValue } from '@tamagui/core'

// Access tokens programmatically
getTokens().size.small.val       // raw value: 10
getTokens().size.small.variable  // CSS var name: var(--size-small)

// getVariable: CSS var on web, raw value on native
getVariable(theme.background)

// getVariableValue: always raw value
getVariableValue(theme.background)
```
