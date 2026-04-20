# Layout Components

## Stacks — XStack, YStack, ZStack

Flex layout primitives. Extend View from `@tamagui/core`.

```bash
npm install @tamagui/stacks  # or use from 'tamagui'
```

```tsx
import { XStack, YStack, ZStack } from 'tamagui'

// Horizontal
<XStack gap="$2">
  <YStack />
  <YStack />
</XStack>

// Vertical
<YStack gap="$3">
  <Text>Hello</Text>
  <Text>World</Text>
</YStack>

// Layered (position: absolute children)
<ZStack>
  <YStack />
  <YStack />
</ZStack>
```

Fuller example:

```tsx
<XStack
  flex={1}
  flexWrap="wrap"
  backgroundColor="#fff"
  hoverStyle={{ backgroundColor: 'red' }}
  $gtSm={{ flexDirection: 'column', flexWrap: 'nowrap' }}
>
  <YStack gap="$3">
    <Text>Hello</Text>
  </YStack>
</XStack>
```

### Stack-specific props

| Prop | Type | Description |
|------|------|-------------|
| `elevation` | `number \| tokens.size` | Natural-looking shadow that expands with size |

All stacks accept all [Tamagui style props](/docs/intro/props).

---

## ScrollView

Extends React Native ScrollView with Tamagui style props.

```bash
npm install @tamagui/scroll-view  # or use from 'tamagui'
```

```tsx
import { ScrollView } from 'tamagui'

<ScrollView maxHeight={300}>
  {/* content */}
</ScrollView>
```

---

## Group — XGroup, YGroup

Groups children with connected border radii.

```bash
npm install @tamagui/group  # or use from 'tamagui'
```

```tsx
import { Button, XGroup, YGroup, Separator, ListItem } from 'tamagui'

// Horizontal group
<XGroup>
  <XGroup.Item>
    <Button>First</Button>
  </XGroup.Item>
  <XGroup.Item>
    <Button>Second</Button>
  </XGroup.Item>
</XGroup>

// Vertical group with separators
<YGroup>
  <YGroup.Item>
    <ListItem title="First" />
  </YGroup.Item>
  <Separator />
  <YGroup.Item>
    <ListItem title="Second" />
  </YGroup.Item>
</YGroup>
```

In v2, children control their own sizing. The `size` prop on Group only adjusts border radius.

### Group props

| Prop | Type | Description |
|------|------|-------------|
| `orientation` | `"horizontal" \| "vertical"` | Layout direction (defaults per XGroup/YGroup) |
| `size` | `SizeTokens` | Border radius of the group container |
| `disabled` | `boolean` | Passes disabled state to children |

### Group.Item props

| Prop | Type | Description |
|------|------|-------------|
| `forcePlacement` | `"first" \| "center" \| "last"` | Override automatic position detection |

**Note:** Automatic first/last detection only works when `Group.Item` is a direct child. For wrapped children, use `forcePlacement` or the `useGroupItem` hook.

---

## Separator

Horizontal or vertical divider line.

```bash
npm install @tamagui/separator  # or use from 'tamagui'
```

```tsx
import { Separator, Paragraph, XStack } from 'tamagui'

<XStack alignItems="center">
  <Paragraph>Blog</Paragraph>
  <Separator alignSelf="stretch" vertical />
  <Paragraph>Docs</Paragraph>
</XStack>
```

Uses `borderWidth` and `borderColor` for styling.

| Prop | Type | Description |
|------|------|-------------|
| `vertical` | `boolean` | Shows separator vertically |

---

## Unspaced

Prevents parent Stack from applying `gap`/`space` to a child.

```tsx
import { Unspaced, YStack, Text } from 'tamagui'

<YStack gap="$4">
  <Text>Has gap above</Text>
  <Unspaced>
    <Text>No gap above this</Text>
  </Unspaced>
  <Text>Has gap above</Text>
</YStack>
```
