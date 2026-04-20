# Typography Components

## Text

Base text component from `@tamagui/core`. Does NOT inherit theme color — use SizableText or Paragraph for themed text.

```tsx
import { Text } from 'tamagui'

<Text color="$white" fontFamily="$body" fontSize={20}
  hoverStyle={{ color: '$colorHover' }}>
  Lorem ipsum
</Text>
```

| Prop | Type | Description |
|------|------|-------------|
| `ellipsis` | `boolean` | Truncate to single line with ellipsis |
| `numberOfLines` | `number` | Clamp text to N lines (uses `-webkit-line-clamp` on web) |

---

## SizableText

Extends Text with the `size` prop. Maps size token to fontSize, lineHeight, fontWeight, letterSpacing from your font config.

```tsx
import { SizableText } from 'tamagui'

<SizableText size="$4">Hello</SizableText>
```

| Prop | Type | Description |
|------|------|-------------|
| `size` | `SizeTokens` | Sets font size + related properties from font config |

---

## Paragraph

Extends SizableText. Renders `<p>` on web, uses theme color, defaults `userSelect: 'auto'`.

```tsx
import { Paragraph } from 'tamagui'

<Paragraph size="$4">Body text with theme color</Paragraph>
<Paragraph ellipsis maxWidth={200}>Truncated text...</Paragraph>
<Paragraph numberOfLines={3}>Clamped to 3 lines...</Paragraph>
```

**Warning:** Renders to `<p>` on web — don't nest them during SSR. Use `SizableText` if you need `<span>`.

---

## Headings — H1–H6, Heading

Extend Paragraph with `fontFamily: '$heading'`. Require `heading` font in config.

```bash
npm install @tamagui/text  # or use from 'tamagui'
```

```tsx
import { H1, H2, H3, H4, H5, H6, Heading } from 'tamagui'

<H1>Heading 1</H1>
<H2>Heading 2</H2>
<Heading>Generic heading</Heading>
```

Font tokens should have keys 1–10 for headings to work automatically.

---

## Inline Text — Strong, Em, Span

Semantic inline text styling. Render to their HTML equivalents on web.

```tsx
import { Strong, Em, Span, Paragraph } from '@tamagui/text'

<Paragraph>
  This is <Strong>bold</Strong>, <Em>italic</Em>, and
  <Span color="$blue10">colored</Span>.
</Paragraph>
```

---

## Anchor

Link component extending SizableText, renders `<a>` on web.

```bash
npm install @tamagui/text  # or use from 'tamagui'
```

```tsx
import { Anchor } from 'tamagui'

<Anchor href="https://example.com" target="_blank">Link</Anchor>
```

---

## HTML Elements

Semantic layout components mapping to HTML elements. Extend View.

```bash
npm install @tamagui/elements  # or use from 'tamagui'
```

Available: `Section`, `Article`, `Main`, `Header`, `Aside`, `Footer`, `Nav`

```tsx
import { Main, Header, Footer, Nav } from 'tamagui'

<Main flex={1}>
  <Header>...</Header>
  <Nav>...</Nav>
  <Footer>...</Footer>
</Main>
```
