# Feedback Components

## Dialog

Modal floating window. Automatically stacks above other overlays.

```bash
npm install @tamagui/dialog  # or use from 'tamagui'
```

### Anatomy

```tsx
import { Dialog } from 'tamagui'

<Dialog>
  <Dialog.Trigger />
  <Dialog.Portal>
    <Dialog.Overlay />
    <Dialog.Content>
      <Dialog.Title />
      <Dialog.Description />
      <Dialog.Close />
    </Dialog.Content>
  </Dialog.Portal>
</Dialog>
```

### With Sheet adaptation (mobile)

```tsx
<Dialog>
  <Dialog.Trigger />
  <Dialog.Portal>
    <Dialog.Overlay />
    <Dialog.Content>
      <Dialog.Title />
      <Dialog.Description />
      <Dialog.Close />
    </Dialog.Content>
  </Dialog.Portal>

  <Dialog.Adapt when="max-md">
    <Dialog.Sheet>
      <Dialog.Sheet.Frame>
        <Dialog.Adapt.Contents />
      </Dialog.Sheet.Frame>
      <Dialog.Sheet.Overlay />
    </Dialog.Sheet>
  </Dialog.Adapt>
</Dialog>
```

### Scoping (performance)

Mount Dialog at root, trigger from deep in the tree:

```tsx
// _layout.tsx
<Dialog scope="user-profile">
  <Dialog.Portal>...</Dialog.Portal>
  {children}
</Dialog>

// deeply nested
<Dialog.Trigger scope="user-profile">
  <Button>Open</Button>
</Dialog.Trigger>
```

Key props:

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `open` | `boolean` | — | Controlled open state |
| `onOpenChange` | `(open: boolean) => void` | — | Open/close callback |
| `modal` | `boolean` | `true` | Portal to root |
| `keepChildrenMounted` | `boolean` | `false` | Keep content mounted when closed |

Prevent outside dismissal:

```tsx
<Dialog.Content onPointerDownOutside={(e) => e.preventDefault()}>
```

---

## AlertDialog

Like Dialog but with stricter accessibility for interrupting prompts.

```bash
npm install @tamagui/alert-dialog  # or use from 'tamagui'
```

```tsx
import { AlertDialog, Button } from 'tamagui'

<AlertDialog>
  <AlertDialog.Trigger asChild>
    <Button>Delete</Button>
  </AlertDialog.Trigger>
  <AlertDialog.Portal>
    <AlertDialog.Overlay />
    <AlertDialog.Content>
      <AlertDialog.Title>Are you sure?</AlertDialog.Title>
      <AlertDialog.Description>This cannot be undone.</AlertDialog.Description>
      <AlertDialog.Cancel asChild><Button>Cancel</Button></AlertDialog.Cancel>
      <AlertDialog.Action asChild><Button theme="red">Delete</Button></AlertDialog.Action>
    </AlertDialog.Content>
  </AlertDialog.Portal>
</AlertDialog>
```

Extra sub-components vs Dialog: `AlertDialog.Cancel`, `AlertDialog.Action`, `AlertDialog.Destructive`.
Supports `native` prop for iOS native alert dialog.

---

## Sheet

Bottom sheet that slides up. Supports drag, snap points, gesture handler integration.

```bash
npm install @tamagui/sheet  # or use from 'tamagui'
```

```tsx
import { Sheet } from 'tamagui'

<Sheet open={open} onOpenChange={setOpen} snapPoints={[80, 50]}>
  <Sheet.Overlay />
  <Sheet.Handle />
  <Sheet.Frame>
    <Sheet.ScrollView>{/* scrollable content */}</Sheet.ScrollView>
  </Sheet.Frame>
</Sheet>
```

Key props:

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `open` | `boolean` | — | Controlled state |
| `snapPoints` | `number[]` | `[80, 10]` | % of screen height, most→least visible |
| `position` | `number` | — | Index into snapPoints |
| `dismissOnOverlayPress` | `boolean` | `true` | Close on overlay tap |
| `dismissOnSnapToBottom` | `boolean` | — | Close when snapped to 0 |
| `disableDrag` | `boolean` | — | Disable drag gestures |
| `modal` | `boolean` | — | Portal to root |
| `moveOnKeyboardChange` | `boolean` | `false` | Move up when keyboard opens (native) |

Native gesture handler: install `react-native-gesture-handler` + `import '@tamagui/native/setup-gesture-handler'` for smooth scroll-to-drag handoffs.

---

## Popover

Floating content anchored to a trigger. 12 placement positions.

```bash
npm install @tamagui/popover  # or use from 'tamagui'
```

```tsx
import { Popover, Adapt, Sheet } from 'tamagui'

<Popover placement="bottom">
  <Popover.Trigger />
  <Popover.Content>
    <Popover.Arrow />
    {/* content */}
    <Popover.Close />
  </Popover.Content>

  <Adapt when="max-md">
    <Sheet>
      <Sheet.Overlay />
      <Sheet.Frame>
        <Sheet.ScrollView>
          <Adapt.Contents />
        </Sheet.ScrollView>
      </Sheet.Frame>
    </Sheet>
  </Adapt>
</Popover>
```

Key props:

| Prop | Type | Description |
|------|------|-------------|
| `placement` | `Placement` | 12 positions: top, bottom, left, right + start/end variants |
| `open` / `onOpenChange` | — | Controlled state |
| `hoverable` | `boolean \| UseFloatingProps` | Open on hover |
| `keepChildrenMounted` | `boolean \| "lazy"` | Keep content mounted |
| `stayInFrame` | `ShiftProps \| boolean` | Shift to stay in viewport |
| `allowFlip` | `FlipProps \| boolean` | Flip to other side if no space |
| `offset` | `OffsetOptions` | Distance from trigger |

Scoping works same as Dialog for performance.

Utility functions: `closeOpenPopovers()`, `closeLastOpenedPopover()`, `hasOpenPopovers()`.

---

## Tooltip

Like Popover but simpler — shows on hover/focus with delay.

```bash
npm install @tamagui/tooltip  # or use from 'tamagui'
```

```tsx
import { Tooltip, Button } from 'tamagui'

<Tooltip>
  <Tooltip.Trigger asChild>
    <Button>Hover me</Button>
  </Tooltip.Trigger>
  <Tooltip.Content>
    <Tooltip.Arrow />
    <Paragraph>Tooltip text</Paragraph>
  </Tooltip.Content>
</Tooltip>
```

---

## Menu

Floating action list with nested submenus. Supports native menus (iOS/Android via zeego).

```bash
npm install @tamagui/menu  # or use from 'tamagui'
```

```tsx
import { Menu, Button } from 'tamagui'

<Menu>
  <Menu.Trigger asChild>
    <Button>Actions</Button>
  </Menu.Trigger>
  <Menu.Portal>
    <Menu.Content>
      <Menu.Item onSelect={handleEdit} key="edit">
        <Menu.ItemTitle>Edit</Menu.ItemTitle>
      </Menu.Item>
      <Menu.Separator />
      <Menu.Sub>
        <Menu.SubTrigger>
          <Menu.ItemTitle>More</Menu.ItemTitle>
        </Menu.SubTrigger>
        <Menu.Portal>
          <Menu.SubContent>
            <Menu.Item key="copy" onSelect={handleCopy}>
              <Menu.ItemTitle>Copy</Menu.ItemTitle>
            </Menu.Item>
          </Menu.SubContent>
        </Menu.Portal>
      </Menu.Sub>
    </Menu.Content>
  </Menu.Portal>
</Menu>
```

Sub-components: `Menu.Item`, `Menu.ItemTitle`, `Menu.ItemIcon`, `Menu.ItemImage`, `Menu.ItemSubtitle`, `Menu.CheckboxItem`, `Menu.RadioGroup`, `Menu.RadioItem`, `Menu.ItemIndicator`, `Menu.Label`, `Menu.Separator`, `Menu.Sub`, `Menu.SubTrigger`, `Menu.SubContent`, `Menu.ScrollView`, `Menu.Arrow`.

Native setup: `yarn add zeego @react-native-menu/menu react-native-ios-context-menu react-native-ios-utilities sf-symbols-typescript` then `import '@tamagui/native/setup-zeego'`.

**Styling note:** Use `focusStyle` (not `hoverStyle`) for item highlights — prevents double-highlighting with keyboard navigation.

---

## ContextMenu

Same API as Menu but triggers on right-click (web) / long-press (native).

```bash
npm install @tamagui/context-menu  # or use from 'tamagui'
```

Same anatomy as Menu with `ContextMenu.*` prefix.

---

## Toast

Feedback notifications with auto-dismiss, swipe, and native support.

```bash
npm install @tamagui/toast  # or use from 'tamagui'
```

### Setup

```tsx
// in app root
<ToastProvider>
  {/* your app */}
  <ToastViewport />
</ToastProvider>
```

### Usage with hooks

```tsx
import { useToastController, useToastState, Toast } from '@tamagui/toast'

// Show toast
const toast = useToastController()
toast.show('Saved!', { message: 'Your changes were saved.' })

// Render current toast
const CurrentToast = () => {
  const toast = useToastState()
  if (!toast || toast.isHandledNatively) return null
  return (
    <Toast key={toast.id} duration={toast.duration}>
      <Toast.Title>{toast.title}</Toast.Title>
      <Toast.Description>{toast.message}</Toast.Description>
    </Toast>
  )
}
```

Native toasts: `yarn add burnt` then `import '@tamagui/native/setup-burnt'`, use `<ToastProvider native>`.

Custom data with TypeScript: augment `CustomData` interface in `@tamagui/toast`.

---

## Spinner

Loading indicator.

```bash
npm install @tamagui/spinner  # or use from 'tamagui'
```

```tsx
import { Spinner } from 'tamagui'

<Spinner size="large" color="$color" />
```

---

## Progress

Progress bar.

```bash
npm install @tamagui/progress  # or use from 'tamagui'
```

```tsx
import { Progress } from 'tamagui'

<Progress value={60} size="$4">
  <Progress.Indicator animation="bouncy" />
</Progress>
```

| Prop | Type | Description |
|------|------|-------------|
| `value` | `number` | 0–100 progress value |
| `max` | `number` | Maximum value (default 100) |
