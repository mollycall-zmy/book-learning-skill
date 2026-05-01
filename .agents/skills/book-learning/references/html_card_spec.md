# HTML Card Spec

Use inline HTML cards only when they make `outputs/reading_notes.md` easier to scan in Markdown or Obsidian.

## Use Cases

- Book one-liner card near the top of the note
- Process flow card for step-based methods or reasoning paths
- Core framework grid under `## 全书核心框架`
- Comparison cards for opposing interpretations, modes, causes, or tradeoffs

Ordinary chapter notes should remain Markdown unless a visual component clearly improves readability.

## Visual Tokens

- Outer background: `linear-gradient(135deg, #FAFAFA 0%, #F2F0EB 100%)`
- Outer padding: `28px`
- Content card background: `#FFFFFF`
- Content card radius: `12px`
- Content card shadow: `box-shadow: 0 4px 20px rgba(0,0,0,0.05)`
- Gold emphasis: `linear-gradient(135deg, #D4AF7A 0%, #CFA76F 100%)`
- Small heading color: `#CFA76F`
- Normal title: `14px`, `#333`, `600`
- Small label: `11px`, `#888`
- Body: `12px`, `#555`, `line-height: 1.6`
- Grid: `grid-template-columns: repeat(4, 1fr); gap: 16px`

## Card Differentiation Principle

The design system is unified, but card types must be visually distinguishable.

Unified:

- Warm white gradient background
- Gold accent
- Black / gray typography
- Rounded corners
- Light visual weight
- Inline styles

Differentiated:

- One-liner: flat gradient panel, no inner white card
- Process flow: lightweight nodes, thin border, no shadow
- Core framework: stable knowledge cards, light shadow, optional thin gold divider
- Comparison: two-column contrast layout with subtle background difference and center divider

Do not create difference by adding noise, new colors, heavy shadows, or decorative ornaments.

## Rules

- Use inline style only.
- Do not use external CSS.
- Do not use JavaScript.
- Do not use dark card backgrounds.
- Do not use heavy shadows such as high-opacity black shadows.
- Do not use top border decoration.
- Do not use full border declarations outside lightweight process nodes.
- Use the warm gradient only on outer containers.
- Use white cards for content blocks.
- Use gold gradient only for key process nodes.
- Avoid large gold areas.

## Component Guidance

- One-liner cards should be the most restrained component: flat gradient panel, larger text, no inner card, no shadow.
- Process nodes should feel lighter than knowledge cards: use translucent white, a thin neutral border, and no shadow on normal nodes.
- Core framework cards should feel stable: use white cards, light shadow, and a subtle gold divider under the title.
- Comparison cards should make the relationship obvious: use two columns, subtle background differences, and a center divider.
