<p align="center">
  <img src="docs/images/cover.png" alt="book-learning-skill cover" width="100%">
</p>

<h1 align="center">book-learning-skill</h1>

<p align="center">
  <strong>An open Agent Skill for systematic whole-book learning</strong><br>
  <sub>
    By <a href="https://mollycall.cn">MW · 美未职造</a>
    &mdash;
    Structure → Chapters → Audit → Knowledge Cards
  </sub>
</p>

<p align="center">
  <a href="./LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green.svg">
  </a>
  <a href="./README.md">
    <img alt="README Chinese" src="https://img.shields.io/badge/README-Chinese-red.svg">
  </a>
  <img alt="Agent Skill" src="https://img.shields.io/badge/Agent%20Skill-book--learning-purple.svg">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-blue.svg">
</p>

**book-learning-skill** is an open Agent Skill that turns a whole book from PDF / EPUB / DOCX / HTML into auditable, traceable, reusable structured knowledge assets.

It is not a "read and summarize" shortcut. It guides an Agent through table-of-contents extraction, chapter notes, omission audits, layered summaries, and atomic knowledge cards.

> Produced by [MW · 美未职造](https://mollycall.cn)  
> License: MIT  
> Status: v0.1.x MVP

## Contents

- [What Problem It Solves](#what-problem-it-solves)
- [Core Principles](#core-principles)
- [How It Works](#how-it-works)
- [Skill](#skill)
- [Features](#features)
- [Supported Formats](#supported-formats)
- [Outputs](#outputs)
- [Quick Start](#quick-start)
- [Local Tests](#local-tests)
- [Using It With An Agent](#using-it-with-an-agent)
- [Roadmap](#roadmap)
- [License](#license)
- [Brand Notice](#brand-notice)
- [Contributing](#contributing)

## What Problem It Solves

Whole-book learning is hard for Agents because long books cannot usually fit into one prompt. Naive summaries often skip chapters, flatten details, and lose context. Notes also become less useful when claims cannot be traced back to chapters or line ranges.

This Skill turns whole-book learning into an executable workflow: preserve structure, split chapters, write chapter notes, audit omissions, and only then create summaries and atomic knowledge cards.

## Core Principles

> Structure preservation > Chapter understanding > Detail retention > Source traceability > Layered summary > Cross-chapter synthesis > Atomic knowledge extraction

- **Structure preservation**: identify the TOC and chapter boundaries before summarizing.
- **Chapter understanding**: digest each chapter independently.
- **Detail retention**: keep definitions, data, examples, constraints, counterexamples, and surprising claims.
- **Source traceability**: every claim should trace back to a chapter or line range.
- **Layered summary**: compress gradually from chapter notes to book summary to cards.
- **Cross-chapter synthesis**: synthesize themes only after chapter notes are complete.
- **Atomic extraction**: each card should preserve one reusable idea.

## How It Works

```text
You / User
   │
   ▼
Agent (Codex / Hermes / Cursor / OpenClaw)
   │
   ▼
book-learning-skill
   ├── Detect file format
   ├── PDF / EPUB / DOCX / HTML → Markdown
   ├── Extract TOC + chapter boundaries
   ├── Split by chapter
   ├── SQ3R chapter reading and notes
   ├── Chapter omission audit
   ├── Layered summary L0 → L4
   └── Generate atomic knowledge cards
   │
   ▼
Knowledge Base / Notes / Atomic Knowledge Cards
```

The point is not simply faster summarization. The point is structure, auditability, and traceability for long-text work.

## Skill

| Skill | Description | Typical Triggers |
| --- | --- | --- |
| **book-learning** | Learn a whole book through conversion, TOC extraction, chapter notes, omission audits, layered summaries, and atomic knowledge cards | `study this book` `read this EPUB` `turn this PDF into knowledge cards` `学习这本书` `喂你一本书` |

## Features

- [x] PDF / EPUB / DOCX / HTML / Markdown workflow
- [x] Convert documents to Markdown
- [x] Extract TOC from Markdown headings
- [x] Output chapter title, heading level, and line ranges
- [x] Split chapter files from TOC
- [x] Audit missing chapter files and note files
- [x] Provide templates for chapter notes, book summaries, and cards
- [x] Provide a standard Agent Skill directory
- [ ] Generate chapter note skeletons automatically
- [ ] OCR workflow orchestration
- [ ] Resumable progress for large books
- [ ] Generate knowledge card indexes

## Supported Formats

| Input | Status | Method |
| --- | --- | --- |
| `.md` | Native | Extract TOC and split directly |
| `.pdf` | Supported | Convert with PyMuPDF4LLM |
| `.epub` | Supported | Convert with Pandoc |
| `.docx` | Supported | Convert with Pandoc |
| `.html` / `.htm` | Supported | Convert with Pandoc |
| Scanned PDF | Indirect | OCR first, then PDF → Markdown |
| `.caj` / `.nh` / `.kdh` | Not directly supported | Convert to PDF first |

## Outputs

| Output | Description |
| --- | --- |
| `toc.json` | TOC, chapter levels, and line ranges |
| `chapters/` | Chapter-level Markdown files |
| `notes/` | SQ3R chapter notes |
| `audit.json` | Chapter omission audit report |
| `book_summary.md` | Layered book summary |
| `knowledge_cards/` | Atomic knowledge cards |
| `index.md` | Knowledge base index, planned for v0.2.0 |

## Quick Start

### Use As An Agent Skill

Open this repository as a project, or place `.agents/skills/book-learning/` in your Agent workspace.

Then ask:

> Read this book chapter by chapter and generate traceable knowledge cards.

The Agent should follow `.agents/skills/book-learning/SKILL.md`.

### Run Scripts Manually

```bash
git clone https://github.com/mollycall-zmy/book-learning-skill.git
cd book-learning-skill

python3 -m pip install -r requirements.txt
python3 .agents/skills/book-learning/scripts/check_tools.py
```

Run the synthetic sample:

```bash
python3 .agents/skills/book-learning/scripts/extract_toc.py examples/sample_book.md --out outputs/toc.json
python3 .agents/skills/book-learning/scripts/split_chapters.py examples/sample_book.md --toc outputs/toc.json --out outputs/chapters
python3 .agents/skills/book-learning/scripts/audit_chapters.py --toc outputs/toc.json --chapters outputs/chapters --notes outputs/notes --out outputs/audit.json
```

Use your own PDF / EPUB / DOCX / HTML:

```bash
python3 .agents/skills/book-learning/scripts/convert_to_md.py path/to/your_book.pdf --out outputs/your_book.md
python3 .agents/skills/book-learning/scripts/extract_toc.py outputs/your_book.md --out outputs/toc.json
python3 .agents/skills/book-learning/scripts/split_chapters.py outputs/your_book.md --toc outputs/toc.json --out outputs/chapters
```

Only process files that you legally own or have permission to process. Do not commit copyrighted books, private files, or generated outputs.

## Local Tests

```bash
python3 -m unittest discover -s tests
```

## Using It With An Agent

The repository follows a common Agent Skill layout:

```text
.agents/
└── skills/
    └── book-learning/
        ├── SKILL.md
        ├── references/
        ├── scripts/
        └── assets/
```

The Agent should read `SKILL.md` first, then load these references as needed:

- `references/workflow.md`
- `references/output_schema.md`
- `references/card_rules.md`

## Roadmap

### v0.1.x

- [x] Standard Agent Skill directory
- [x] PDF / EPUB / DOCX / HTML / Markdown conversion entry point
- [x] TOC extraction
- [x] Chapter splitting
- [x] Chapter omission audit
- [x] Chinese README
- [x] Contributing guide

### v0.2.0

- [ ] `check_tools.py --install`
- [ ] Generate chapter note skeletons automatically
- [ ] `progress.json` resumable progress
- [ ] OCR orchestration
- [ ] Knowledge card index generation
- [ ] Obsidian / Logseq output adapters

## License

This repository is released under the MIT License. See [LICENSE](./LICENSE) for details.

## Brand Notice

The source code and general documentation are open under the MIT License.

Brand assets, cover images, logos, and the “MW · 美未职造” brand identity are not included in the default open-source license unless explicitly stated otherwise.

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md).

---

<p align="center">
  <strong>MW · 美未职造</strong><br>
  <a href="https://mollycall.cn">mollycall.cn</a> ·
  <a href="mailto:business@mollycall.cn">business@mollycall.cn</a>
</p>
