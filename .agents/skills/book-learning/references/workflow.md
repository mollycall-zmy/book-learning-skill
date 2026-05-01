# Workflow

## Purpose

Turn a whole book into reliable learning artifacts:

1. Preserved structure
2. Complete chapter coverage
3. Chapter-level understanding
4. Traceable summaries
5. Atomic knowledge cards

## Step 0: Receive And Convert

Place the original file under `raw/books/` and treat it as read-only.

Supported MVP inputs:

- `.md`: use directly
- `.pdf`: convert with `pymupdf4llm`
- `.epub`, `.docx`, `.html`, `.htm`: convert with `pandoc`, falling back to `pypandoc` if available

For scanned PDFs, run OCR before conversion. In v0.1.0, OCR is detected but not automated.

## Step 1: Extract TOC

Run `extract_toc.py` on the Markdown file. The output must include:

- Stable chapter id
- Heading title
- Heading level
- Start line
- End line

If the Markdown has no headings, stop and ask for a chapter structure or create a proposed structure for user review.

## Step 2: Review Target Categories

Before creating cards, inspect the existing `knowledge_base/` structure if present. Reuse existing categories when possible.

## Step 3: Split Chapters

Run `split_chapters.py` using the TOC JSON. Each heading range becomes one Markdown file.

Use deterministic filenames based on chapter id and a slugified title.

## Step 4: Read Chapter By Chapter

For each chapter, apply SQ3R:

- Survey: identify the chapter structure and central topic
- Question: write the questions the chapter tries to answer
- Read: extract claims, definitions, evidence, examples, data, and caveats
- Recite: restate the argument in your own words
- Review: note implications, weak points, and links to other chapters

Use `assets/chapter_note_template.md`.

## Step 5: Preserve Details

Do not drop definitions, data, cases, constraints, exceptions, counterexamples, or surprising claims. These details often become the most useful cards.

## Step 6: Layer Summaries

Move from source to abstraction:

- L0: source Markdown
- L1: chapter excerpts or evidence notes
- L2: chapter notes
- L3: full-book summary
- L4: atomic knowledge cards

Never create L3 or L4 before L2 exists for every chapter.

## Step 7: Audit Omissions

Run `audit_chapters.py` before summarizing the whole book. A clean audit means:

- Every TOC entry has a chapter file
- Every chapter file maps to a TOC entry
- Every required chapter has a note file

If any chapter is missing, scan the whole TOC again.

## Step 8: Create Knowledge Cards

Read `references/card_rules.md` first. Each card must contain exactly one idea and cite its source chapter.

## Failure Handling

- Missing converter: run `check_tools.py`, then tell the user which tool is missing.
- Bad TOC: inspect Markdown headings and rerun extraction after improving heading structure.
- Huge book: process chapter batches, but keep one global TOC and audit report.
- OCR quality issue: ask for a better scan or OCR pass before learning.
