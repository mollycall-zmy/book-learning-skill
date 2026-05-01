# HTML Card Spec

Use inline HTML cards only when they make `outputs/reading_notes.md` easier to scan in Markdown or Obsidian.

## Use Cases

- Book one-liner card near the top of the note
- Process flow card for step-based methods or reasoning paths
- Core framework grid under `## 全书核心框架`
- Key model or comparison cards when plain Markdown becomes hard to scan

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

## Rules

- Use inline style only.
- Do not use external CSS.
- Do not use JavaScript.
- Do not use dark card backgrounds.
- Do not use heavy shadows such as high-opacity black shadows.
- Do not use top border decoration.
- Do not use full border declarations.
- Use the warm gradient only on outer containers.
- Use white cards for content blocks.
- Use gold gradient only for key process nodes.
- Avoid large gold areas.
