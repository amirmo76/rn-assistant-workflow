# Data Display Components

## Accordion

Vertically stacked collapsible sections.

```bash
npm install @tamagui/accordion  # or use from 'tamagui'
```

```tsx
import { Accordion, Paragraph, YStack } from 'tamagui'

<Accordion type="multiple" defaultValue={['item-1']}>
  <Accordion.Item value="item-1">
    <Accordion.Header>
      <Accordion.Trigger>
        <Paragraph>Section 1</Paragraph>
      </Accordion.Trigger>
    </Accordion.Header>
    <Accordion.Content>
      <Paragraph>Content 1</Paragraph>
    </Accordion.Content>
  </Accordion.Item>
  <Accordion.Item value="item-2">
    <Accordion.Header>
      <Accordion.Trigger>
        <Paragraph>Section 2</Paragraph>
      </Accordion.Trigger>
    </Accordion.Header>
    <Accordion.Content>
      <Paragraph>Content 2</Paragraph>
    </Accordion.Content>
  </Accordion.Item>
</Accordion>
```

Key props:

| Prop | Type | Description |
|------|------|-------------|
| `type` | `"single" \| "multiple"` | One or many items open |
| `value` / `defaultValue` | `string \| string[]` | Controlled/uncontrolled open items |
| `onValueChange` | `(value) => void` | Change callback |
| `collapsible` | `boolean` | Allow closing all items (single mode) |
| `disabled` | `boolean` | Disable all items |

---

## Avatar

Profile image with fallback.

```bash
npm install @tamagui/avatar  # or use from 'tamagui'
```

```tsx
import { Avatar } from 'tamagui'

<Avatar circular size="$6">
  <Avatar.Image src="https://example.com/avatar.jpg" />
  <Avatar.Fallback backgroundColor="$blue10" />
</Avatar>
```

| Sub-component | Description |
|---------------|-------------|
| `Avatar.Image` | The image, accepts `src` |
| `Avatar.Fallback` | Shown while image loads or on error. `delayMs` to delay showing |

---

## Card

Container with header, footer, and background.

```bash
npm install @tamagui/card  # or use from 'tamagui'
```

```tsx
import { Card, H2, Paragraph, Button, XStack } from 'tamagui'

<Card elevate size="$4" bordered>
  <Card.Header padded>
    <H2>Title</H2>
    <Paragraph>Description</Paragraph>
  </Card.Header>
  <Card.Footer padded>
    <XStack flex={1} />
    <Button size="$3">Action</Button>
  </Card.Footer>
  <Card.Background>
    <Image src="..." objectFit="cover" width="100%" height="100%" />
  </Card.Background>
</Card>
```

| Sub-component | Description |
|---------------|-------------|
| `Card.Header` | Top section. `padded` prop adds default padding |
| `Card.Footer` | Bottom section. `padded` prop |
| `Card.Background` | Behind header/footer, absolutely positioned |

---

## Image

Cross-platform image with web-first API. No react-native-web dependency.

```bash
npm install @tamagui/image  # or use from 'tamagui'
```

```tsx
import { Image } from 'tamagui'

<Image src="https://example.com/photo.jpg" width={300} height={200} alt="Photo" />
```

| Prop | Type | Description |
|------|------|-------------|
| `src` | `string` | Image URL (required) |
| `alt` | `string` | Accessibility text |
| `objectFit` | `CSS.ObjectFit` | Resize mode (alternative to `resizeMode`) |
| `onLoad` | `function` | Load callback |
| `onError` | `function` | Error callback |

Accepts all web `<img>` props on web, all RN Image props on native.

---

## ListItem

Pre-built list row with icon, title, subtitle, and trailing content.

```bash
npm install @tamagui/list-item  # or use from 'tamagui'
```

```tsx
import { ListItem, Separator, YGroup } from 'tamagui'
import { ChevronRight } from '@tamagui/lucide-icons-2'

<YGroup bordered>
  <YGroup.Item>
    <ListItem
      title="Settings"
      subTitle="Manage your account"
      iconAfter={ChevronRight}
      pressTheme
    />
  </YGroup.Item>
  <Separator />
  <YGroup.Item>
    <ListItem title="About" iconAfter={ChevronRight} pressTheme />
  </YGroup.Item>
</YGroup>
```

| Prop | Type | Description |
|------|------|-------------|
| `title` | `ReactNode` | Main text |
| `subTitle` | `ReactNode` | Secondary text |
| `icon` | `ReactNode \| FC` | Leading icon |
| `iconAfter` | `ReactNode \| FC` | Trailing icon |
| `size` | `SizeTokens` | Scales the component |
| `pressTheme` | `boolean` | Apply press theme on interaction |

---

## Tabs

Manage sub-pages with tab navigation.

```bash
npm install @tamagui/tabs  # or use from 'tamagui'
```

```tsx
import { SizableText, Tabs, H5 } from 'tamagui'

<Tabs defaultValue="tab1" width={400}>
  <Tabs.List>
    <Tabs.Tab value="tab1">
      <SizableText>Tab 1</SizableText>
    </Tabs.Tab>
    <Tabs.Tab value="tab2">
      <SizableText>Tab 2</SizableText>
    </Tabs.Tab>
  </Tabs.List>

  <Tabs.Content value="tab1">
    <H5>Tab 1 content</H5>
  </Tabs.Content>
  <Tabs.Content value="tab2">
    <H5>Tab 2 content</H5>
  </Tabs.Content>
</Tabs>
```

Key props:

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` / `defaultValue` | `string` | — | Selected tab |
| `onValueChange` | `(value: string) => void` | — | Change callback |
| `orientation` | `"horizontal" \| "vertical"` | `horizontal` | Layout direction |
| `activationMode` | `"manual" \| "automatic"` | `manual` | Focus vs click activation |

Headless: `useTabs` from `@tamagui/tabs-headless` for custom implementations.

Tabs.Tab supports `activeStyle` and `activeTheme` for selected state styling.
