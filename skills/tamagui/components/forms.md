# Form Components

## Button

Extends Tamagui View with press handling, icons, size, and theme support.

```bash
npm install @tamagui/button  # or use from 'tamagui'
```

```tsx
import { Button } from 'tamagui'
import { Activity } from '@tamagui/lucide-icons-2'

<Button>Label</Button>
<Button size="$4" theme="blue" icon={Activity}>With Icon</Button>
<Button size="$3" variant="outlined">Outlined</Button>
<Button disabled opacity={0.5}>Disabled</Button>
```

Key props:

| Prop | Type | Description |
|------|------|-------------|
| `size` | `SizeTokens` | Scales padding, font, icon, border radius |
| `theme` | `string` | Apply a sub-theme |
| `icon` | `ReactNode \| FC` | Icon before label |
| `iconAfter` | `ReactNode \| FC` | Icon after label |
| `scaleIcon` | `number` | Scale icon relative to size |
| `variant` | `"outlined"` | Outlined style variant |
| `disabled` | `boolean` | Disables interaction |

---

## Input

Web-first single-line text input. Uses HTML attributes with automatic native mapping.

```bash
npm install @tamagui/input  # or use from 'tamagui'
```

```tsx
import { Input } from 'tamagui'

<Input placeholder="Enter text..." size="$4" />
<Input type="password" />
<Input type="email" />
<Input type="tel" />
```

Cross-platform type mapping:

| Web `type` | Native behavior |
|------------|----------------|
| `password` | `secureTextEntry={true}` |
| `email` | `keyboardType="email-address"` |
| `tel` | `keyboardType="phone-pad"` |
| `number` | `keyboardType="numeric"` |

Key props:

| Prop | Type | Description |
|------|------|-------------|
| `size` | `SizeTokens` | Scales the input |
| `type` | `"text" \| "password" \| "email" \| "tel" \| "number" \| "url" \| "search"` | HTML type, auto-maps to native keyboard |
| `enterKeyHint` | `"done" \| "go" \| "next" \| "search" \| "send"` | Return key label |
| `onSubmitEditing` | `(e) => void` | Called on enter/return |

---

## TextArea

Multi-line text input. Same API as Input plus `rows`.

```tsx
import { TextArea } from 'tamagui'

<TextArea placeholder="Long text..." rows={4} />
```

---

## Checkbox

Toggle state with indicator icon.

```bash
npm install @tamagui/checkbox  # or use from 'tamagui'
```

```tsx
import { Check } from '@tamagui/lucide-icons-2'
import { Checkbox } from 'tamagui'

<Checkbox size="$4">
  <Checkbox.Indicator>
    <Check />
  </Checkbox.Indicator>
</Checkbox>
```

Key props:

| Prop | Type | Description |
|------|------|-------------|
| `checked` | `boolean` | Controlled state |
| `defaultChecked` | `boolean` | Uncontrolled default |
| `onCheckedChange` | `(checked: boolean \| "indeterminate") => void` | State change callback |
| `native` | `boolean` | Render native checkbox on web |
| `scaleSize` | `number` | Scale checkbox (default 0.5) |

### Checkbox.Indicator

Contains the check icon. Shows when checked.

| Prop | Type | Description |
|------|------|-------------|
| `forceMount` | `boolean` | Keep mounted for animations |

Headless: `useCheckbox` from `@tamagui/checkbox-headless` for custom implementations without Tamagui dependency.

---

## RadioGroup

```bash
npm install @tamagui/radio-group  # or use from 'tamagui'
```

```tsx
import { RadioGroup, Label, XStack, YStack } from 'tamagui'

<RadioGroup defaultValue="opt1">
  <YStack gap="$2">
    <XStack alignItems="center" gap="$2">
      <RadioGroup.Item value="opt1" id="opt1" size="$3">
        <RadioGroup.Indicator />
      </RadioGroup.Item>
      <Label htmlFor="opt1">Option 1</Label>
    </XStack>
    <XStack alignItems="center" gap="$2">
      <RadioGroup.Item value="opt2" id="opt2" size="$3">
        <RadioGroup.Indicator />
      </RadioGroup.Item>
      <Label htmlFor="opt2">Option 2</Label>
    </XStack>
  </YStack>
</RadioGroup>
```

Key props on RadioGroup: `value`, `defaultValue`, `onValueChange`, `required`, `name`, `native`.

---

## Switch

Toggle between two states.

```bash
npm install @tamagui/switch  # or use from 'tamagui'
```

```tsx
import { Switch } from 'tamagui'

<Switch size="$4">
  <Switch.Thumb animation="bouncy" />
</Switch>
```

| Prop | Type | Description |
|------|------|-------------|
| `checked` | `boolean` | Controlled state |
| `defaultChecked` | `boolean` | Uncontrolled default |
| `onCheckedChange` | `(checked: boolean) => void` | Change callback |
| `native` | `NativeValue` | Render native Switch on mobile |

---

## Slider

Range selection control.

```bash
npm install @tamagui/slider  # or use from 'tamagui'
```

```tsx
import { Slider } from 'tamagui'

<Slider defaultValue={[50]} max={100} step={1} size="$4">
  <Slider.Track>
    <Slider.TrackActive />
  </Slider.Track>
  <Slider.Thumb index={0} circular elevate />
</Slider>
```

| Prop | Type | Description |
|------|------|-------------|
| `value` | `number[]` | Controlled value |
| `defaultValue` | `number[]` | Uncontrolled default |
| `onValueChange` | `(value: number[]) => void` | Change callback |
| `min` | `number` | Minimum value |
| `max` | `number` | Maximum value |
| `step` | `number` | Step increment |
| `orientation` | `"horizontal" \| "vertical"` | Layout direction |

---

## Select

Dropdown menu for choosing from options. On native, use Adapt + Sheet.

```bash
npm install @tamagui/select  # or use from 'tamagui'
```

```tsx
import { Select, Adapt, Sheet } from 'tamagui'

<Select defaultValue="apple">
  <Select.Trigger>
    <Select.Value placeholder="Pick fruit" />
  </Select.Trigger>

  <Adapt when="max-md" platform="touch">
    <Sheet>
      <Sheet.Frame>
        <Adapt.Contents />
      </Sheet.Frame>
      <Sheet.Overlay />
    </Sheet>
  </Adapt>

  <Select.Content>
    <Select.Viewport>
      <Select.Group>
        <Select.Label>Fruits</Select.Label>
        <Select.Item index={0} value="apple">
          <Select.ItemText>Apple</Select.ItemText>
        </Select.Item>
        <Select.Item index={1} value="orange">
          <Select.ItemText>Orange</Select.ItemText>
        </Select.Item>
      </Select.Group>
    </Select.Viewport>
  </Select.Content>
</Select>
```

Performance: Use `lazyMount` + `renderValue` for pages with many Selects.

---

## Label

Accessible label for form controls.

```bash
npm install @tamagui/label  # or use from 'tamagui'
```

```tsx
import { Label, Input, XStack } from 'tamagui'

<XStack alignItems="center" gap="$2">
  <Label htmlFor="name">Name</Label>
  <Input id="name" />
</XStack>
```

---

## Form

HTML form wrapper with submit handling.

```bash
npm install @tamagui/form  # or use from 'tamagui'
```

```tsx
import { Form, Button, Input } from 'tamagui'

<Form onSubmit={() => console.log('submitted')}>
  <Input />
  <Form.Trigger asChild>
    <Button>Submit</Button>
  </Form.Trigger>
</Form>
```

---

## ToggleGroup

Group of toggle buttons, single or multiple selection.

```bash
npm install @tamagui/toggle-group  # or use from 'tamagui'
```

```tsx
import { ToggleGroup } from 'tamagui'

<ToggleGroup type="single" defaultValue="center">
  <ToggleGroup.Item value="left"><Text>Left</Text></ToggleGroup.Item>
  <ToggleGroup.Item value="center"><Text>Center</Text></ToggleGroup.Item>
  <ToggleGroup.Item value="right"><Text>Right</Text></ToggleGroup.Item>
</ToggleGroup>
```

| Prop | Type | Description |
|------|------|-------------|
| `type` | `"single" \| "multiple"` | Selection mode |
| `value` | `string \| string[]` | Controlled value |
| `onValueChange` | `(val) => void` | Change callback |
| `orientation` | `"horizontal" \| "vertical"` | Layout direction |
| `disabled` | `boolean` | Disables all items |
