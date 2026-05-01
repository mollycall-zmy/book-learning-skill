# Reading Notes Section Template

Use this compact section format inside `outputs/reading_notes.md`.

Do not create separate `.notes.md` files by default.

## HTML Card Components

Use these inline HTML components only for high-level visual sections:

- Book one-liner
- Process flow
- Core framework grid
- Key models or comparison frameworks

Keep ordinary chapter notes in Markdown unless visualization improves readability.

Strictly avoid:

- Top border declarations
- Full border declarations
- Dark card backgrounds
- Heavy high-opacity black shadows
- Large gold backgrounds
- External CSS classes
- External CSS files
- JavaScript

## Component 1: Book One-Liner

Use this near the top of `outputs/reading_notes.md`. It replaces the old callout style for the book's core claim.

```html
<div style="background: linear-gradient(135deg, #FAFAFA 0%, #F2F0EB 100%); padding: 28px; border-radius: 16px; margin: 24px 0;">
  <div style="background: #FFFFFF; border-radius: 12px; padding: 22px 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
    <div style="font-size: 11px; color: #CFA76F; font-weight: 600; letter-spacing: 0.08em; margin-bottom: 10px;">
      全书一句话
    </div>
    <div style="font-size: 18px; line-height: 1.7; color: #222; font-weight: 600;">
      这里写全书最核心的主张：用一句话说明这本书到底在讲什么。
    </div>
  </div>
</div>
```

## Component 2: Process Flow

Use this for step-by-step methods, reasoning paths, model paths, or a stable replacement for complex Mermaid diagrams.

```html
<div style="background: linear-gradient(135deg, #FAFAFA 0%, #F2F0EB 100%); padding: 28px; border-radius: 16px; margin: 24px 0;">
  <div style="font-size: 14px; color: #333; font-weight: 600; margin-bottom: 18px;">
    核心流程
  </div>
  <div style="display: flex; align-items: stretch; gap: 10px; margin-bottom: 18px;">
    <div style="flex: 1; background: #FFFFFF; border-radius: 12px; padding: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
      <div style="font-size: 11px; color: #888; margin-bottom: 6px;">Step 1</div>
      <div style="font-size: 14px; color: #333; font-weight: 600; margin-bottom: 8px;">识别问题</div>
      <div style="font-size: 12px; color: #555; line-height: 1.6;">说明第一步的核心动作。</div>
    </div>
    <div style="display: flex; align-items: center; color: #CFA76F; font-size: 18px; font-weight: 600;">→</div>
    <div style="flex: 1; background: linear-gradient(135deg, #D4AF7A 0%, #CFA76F 100%); border-radius: 12px; padding: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
      <div style="font-size: 11px; color: rgba(255,255,255,0.8); margin-bottom: 6px;">Key Step</div>
      <div style="font-size: 14px; color: #FFFFFF; font-weight: 600; margin-bottom: 8px;">关键转折</div>
      <div style="font-size: 12px; color: rgba(255,255,255,0.92); line-height: 1.6;">说明最关键的判断或行动。</div>
    </div>
    <div style="display: flex; align-items: center; color: #CFA76F; font-size: 18px; font-weight: 600;">→</div>
    <div style="flex: 1; background: #FFFFFF; border-radius: 12px; padding: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
      <div style="font-size: 11px; color: #888; margin-bottom: 6px;">Step 3</div>
      <div style="font-size: 14px; color: #333; font-weight: 600; margin-bottom: 8px;">形成结论</div>
      <div style="font-size: 12px; color: #555; line-height: 1.6;">说明最后得到的结果。</div>
    </div>
  </div>
  <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px;">
    <div style="background: #FFFFFF; border-radius: 12px; padding: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
      <div style="font-size: 14px; color: #333; font-weight: 600; margin-bottom: 8px;">常见误区</div>
      <div style="font-size: 12px; color: #555; line-height: 1.6;">这里写容易误解或错误执行的地方。</div>
    </div>
    <div style="background: #FFFFFF; border-radius: 12px; padding: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
      <div style="font-size: 14px; color: #333; font-weight: 600; margin-bottom: 8px;">正确理解</div>
      <div style="font-size: 12px; color: #555; line-height: 1.6;">这里写更准确的理解方式。</div>
    </div>
  </div>
</div>
```

## Component 3: Core Framework Grid

Use this under `## 全书核心框架` for 3-8 core models, concepts, or methods. Default to a 4-column grid and add one full-width relationship summary when useful.

```html
<div style="background: linear-gradient(135deg, #FAFAFA 0%, #F2F0EB 100%); padding: 28px; border-radius: 16px; margin: 24px 0;">
  <div style="font-size: 14px; color: #333; font-weight: 600; margin-bottom: 18px;">
    全书核心框架
  </div>
  <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 16px;">
    <div style="background: #FFFFFF; border-radius: 12px; padding: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
      <div style="font-size: 11px; color: #888; margin-bottom: 6px;">Framework 01</div>
      <div style="font-size: 14px; color: #333; font-weight: 600; margin-bottom: 8px;">框架一</div>
      <div style="font-size: 12px; color: #555; line-height: 1.6;">说明框架一的作用和含义。</div>
    </div>
    <div style="background: #FFFFFF; border-radius: 12px; padding: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
      <div style="font-size: 11px; color: #888; margin-bottom: 6px;">Framework 02</div>
      <div style="font-size: 14px; color: #333; font-weight: 600; margin-bottom: 8px;">框架二</div>
      <div style="font-size: 12px; color: #555; line-height: 1.6;">说明框架二的作用和含义。</div>
    </div>
    <div style="background: #FFFFFF; border-radius: 12px; padding: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
      <div style="font-size: 11px; color: #888; margin-bottom: 6px;">Framework 03</div>
      <div style="font-size: 14px; color: #333; font-weight: 600; margin-bottom: 8px;">框架三</div>
      <div style="font-size: 12px; color: #555; line-height: 1.6;">说明框架三的作用和含义。</div>
    </div>
    <div style="background: #FFFFFF; border-radius: 12px; padding: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
      <div style="font-size: 11px; color: #888; margin-bottom: 6px;">Framework 04</div>
      <div style="font-size: 14px; color: #333; font-weight: 600; margin-bottom: 8px;">框架四</div>
      <div style="font-size: 12px; color: #555; line-height: 1.6;">说明框架四的作用和含义。</div>
    </div>
  </div>
  <div style="background: #FFFFFF; border-radius: 12px; padding: 18px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
    <div style="font-size: 14px; color: #333; font-weight: 600; margin-bottom: 8px;">总体关系</div>
    <div style="font-size: 12px; color: #555; line-height: 1.6;">这里说明这些框架之间的关系，以及它们如何共同构成本书的核心观点。</div>
  </div>
</div>
```

## Ordinary Chapter Section

### {章节标题}

**核心定义/主张**：用 1-2 句话说明本章最核心的观点。[[raw/books/示例书#{章节标题}|🔗]]

**关键框架**：

- 框架 1：说明其结构和含义。[[raw/books/示例书#{章节标题}|🔗]]
- 框架 2：说明其结构和含义。[[raw/books/示例书#{章节标题}|🔗]]

如果没有明确框架，可以省略 `关键框架`，不要硬填。

**核心结论**：用 1-2 句话写出作者在本章得出的最重要结论。[[raw/books/示例书#{章节标题}|🔗]]

**支撑证据**：

- 证据 1：最有力的数据、研究、案例或论证链。
- 证据 2：如果有第二个强证据再补充。

Notes:

- Backlinks use `[[raw/books/{书名}#{标题}|🔗]]`.
- Each chapter section must have at least one source backlink.
- Recommended backlink density: 3-5 per chapter section.
- If `关键框架` exists, each framework item should include a backlink.
- Tables must start at the beginning of the line.
- Tables must have a blank line before them.
- Tables must not be inside lists or callouts.
- Target length: 15-25 lines per chapter.
- Extract definitions, frameworks, conclusions, and evidence - not stories.
