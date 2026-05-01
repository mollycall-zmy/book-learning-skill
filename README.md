<h1 align="center">book-learning-skill</h1>

<p align="center">
  <strong>让 AI Agent 系统性学习整本书的开源技能</strong><br>
  <sub>
    By <a href="https://mollycall.cn">MW · 美未职造</a>
    &mdash;
    结构保存 → 逐章消化 → 审计防漏 → 完整阅读笔记
  </sub>
</p>

<p align="center">
  <a href="./LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green.svg">
  </a>
  <a href="./README.en.md">
    <img alt="README English" src="https://img.shields.io/badge/README-English-blue.svg">
  </a>
  <img alt="Agent Skill" src="https://img.shields.io/badge/Agent%20Skill-book--learning-purple.svg">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-blue.svg">
</p>

**book-learning-skill** 是一个面向 AI Agent 的开源技能，用来把一本书从 PDF / EPUB / DOCX / HTML / Markdown 源文件逐步整理成一份完整、可读、可审计的 Markdown 阅读笔记。

它不是“读完写个摘要”，而是围绕目录树、逐章阅读、AI 分析、双链回链和内容审计，帮助 Agent 更稳地完成整本书学习。

> 出品：[MW · 美未职造](https://mollycall.cn)  
> License：MIT  
> Status：v0.1.x MVP

## 目录

- [项目简介](#项目简介)
- [这个项目解决什么问题](#这个项目解决什么问题)
- [核心理念](#核心理念)
- [How It Works](#how-it-works)
- [Skill](#skill)
- [当前能力](#当前能力)
- [支持格式](#支持格式)
- [输入与输出](#输入与输出)
- [快速开始](#快速开始)
- [在 Agent 中使用](#在-agent-中使用)
- [仓库结构](#仓库结构)
- [本地测试](#本地测试)
- [License](#license)
- [Contributing](#contributing)

## 项目简介

`book-learning-skill` 是一个标准 Agent Skill 仓库。它把“学习一本书”拆成一组明确步骤：转换文档、提取目录、拆分章节、逐章做笔记、审计遗漏，再产出可追溯的摘要和知识卡片。

本仓库只包含 Skill 指令、脚本、模板、测试和自造示例文件；不包含真实书籍、PDF、EPUB、版权摘录或用户私有文件。

## 这个项目解决什么问题

整本书学习不是一个简单摘要任务。长书通常不能一次性塞给模型，普通摘要又很容易跳章、漏细节、丢上下文。很多读书笔记最后只剩结论，却缺少来源追溯，无法确认某个观点来自哪一章、哪些证据或哪些限定条件。

Agent 在处理长文本时需要明确工作流，而不是自由发挥。这个 Skill 将整本书学习拆成可执行步骤，让 Agent 先保留结构，再逐章理解，最后才做跨章整合。

## 核心理念

> 结构保存 > 章节理解 > 细节保留 > 来源可追溯 > AI 分析 > 单一阅读笔记

- **结构保存**：先识别目录树和章节边界，再开始总结。
- **章节理解**：每章独立消化，避免只读前几章就生成全书结论。
- **细节保留**：定义、数据、案例、限定条件、反例和反常识观点都不能被粗暴压缩。
- **来源可追溯**：每个观点都应能追溯到章节或行号。
- **AI 分析**：每章都要包含跨界关联、适用边界、批判性思考和一句话提炼。
- **单一阅读笔记**：默认只生成一份完整的 `outputs/reading_notes.md`，方便长期阅读和归档。

## How It Works

```text
User → Agent → book-learning skill
             → 转 Markdown → 提取 TOC → 拆分章节
             → 逐章阅读 → reading_notes.md → 内容审计
```

这个流程的关键不是“更快总结”，而是让 Agent 在长文本处理中具备结构感、审计感和可追溯性。

## Skill

| Skill | 描述 | 典型触发词 |
| --- | --- | --- |
| **book-learning** | 系统性学习整本书，完成格式转换、目录提取、逐章阅读、AI 分析、双链回链和阅读笔记审计 | `学习这本书` `读一下这本书` `喂你一本书` `逐章做笔记` `整理成阅读笔记` |

## 当前能力

- [x] 支持 PDF / EPUB / DOCX / HTML / Markdown 工作流
- [x] 将文档统一转换为 Markdown
- [x] 从 Markdown 标题提取目录树
- [x] 输出章节标题、层级、起止行号
- [x] 按目录树拆分章节文件
- [x] 生成单一 `outputs/reading_notes.md`
- [x] 审计阅读笔记是否覆盖章节、AI 分析和双链回链
- [x] 提供阅读笔记章节模板
- [x] 提供 Agent Skill 标准目录结构

## 支持格式

| 输入格式 | 支持状态 | 处理方式 |
| --- | --- | --- |
| `.md` | 原生支持 | 直接提取目录树和拆章 |
| `.pdf` | 支持 | 使用 PyMuPDF4LLM 转 Markdown |
| `.epub` | 支持 | 使用 Pandoc 转 Markdown |
| `.docx` | 支持 | 使用 Pandoc 转 Markdown |
| `.html` / `.htm` | 支持 | 使用 Pandoc 转 Markdown |
| 扫描版 PDF | 间接支持 | 需先 OCR，再进入 PDF → Markdown 流程 |

## 输入与输出

运行时内容默认放在 git 忽略的目录中：

- `raw/books/`：原始书籍文件，只读保存
- `outputs/`：转换后的 Markdown、TOC、章节拆分、阅读笔记和审计报告

主要输出物：

| 输出物 | 说明 |
| --- | --- |
| `toc.json` | 目录树、章节层级、起止行号 |
| `raw/books/{书名}.md` | 原文归档，作为阅读笔记的来源 |
| `outputs/reading_notes.md` | 默认主要输出，一本书对应一份完整阅读笔记 |
| `audit.json` | 阅读笔记审计报告 |

如果用户提供知识库或 Obsidian 路径，最终笔记也可以归档为：

```text
L1-事实与语义/02-📚 知识/{书名}-阅读笔记.md
```

## 快速开始

### 方式一：作为 Agent Skill 使用

把本仓库作为项目打开，或将 `.agents/skills/book-learning/` 放入你的 Agent 工作区。

然后对 Agent 说：

> 喂你一本书，帮我逐章学习，并生成一份完整阅读笔记。

Agent 会根据 `.agents/skills/book-learning/SKILL.md` 执行工作流。

### 方式二：手动运行脚本

```bash
git clone https://github.com/mollycall-zmy/book-learning-skill.git
cd book-learning-skill

python3 -m pip install -r requirements.txt
python3 .agents/skills/book-learning/scripts/check_tools.py
```

使用自造示例书测试：

```bash
python3 .agents/skills/book-learning/scripts/extract_toc.py examples/sample_book.md --out outputs/toc.json
python3 .agents/skills/book-learning/scripts/split_chapters.py examples/sample_book.md --toc outputs/toc.json --out outputs/chapters
python3 .agents/skills/book-learning/scripts/audit_reading_notes.py --toc outputs/toc.json --reading-notes outputs/reading_notes.md --out outputs/audit.json
```

使用你自己的 PDF / EPUB / DOCX / HTML：

```bash
python3 .agents/skills/book-learning/scripts/convert_to_md.py path/to/your_book.pdf --out outputs/your_book.md
python3 .agents/skills/book-learning/scripts/extract_toc.py outputs/your_book.md --out outputs/toc.json
python3 .agents/skills/book-learning/scripts/split_chapters.py outputs/your_book.md --toc outputs/toc.json --out outputs/chapters
```

请只使用你合法拥有或有权处理的书籍文件。不要把版权书籍、私人文件或转换后的输出提交到 Git 仓库。

## 在 Agent 中使用

本仓库遵循 Agent Skill 的常见目录结构：

```text
.agents/
└── skills/
    └── book-learning/
        ├── SKILL.md
        ├── references/
        ├── scripts/
        └── assets/
```

Agent 应优先读取 `SKILL.md`，并在需要详细流程、输出格式或卡片规则时读取：

- `references/workflow.md`
- `references/output_schema.md`
- `scripts/audit_reading_notes.py` 用于审计最终阅读笔记

典型中文触发词：

- 学习这本书
- 读一下这本书
- 喂你一本书
- 帮我逐章消化这个 PDF
- 整理成完整阅读笔记
- 生成可追溯的读书笔记

## 仓库结构

```text
book-learning-skill/
├── README.md
├── README.en.md
├── AGENTS.md
├── CONTRIBUTING.md
├── LICENSE
├── requirements.txt
├── examples/
│   ├── README.md
│   └── sample_book.md
├── tests/
│   ├── test_extract_toc.py
│   ├── test_split_chapters.py
│   └── test_audit_chapters.py
├── docs/
│   ├── README.md
│   └── images/
│       └── cover.png
└── .agents/
    └── skills/
        └── book-learning/
            ├── SKILL.md
            ├── references/
            │   ├── workflow.md
            │   ├── output_schema.md
            │   └── card_rules.md (deprecated)
            ├── scripts/
            │   ├── check_tools.py
            │   ├── convert_to_md.py
            │   ├── extract_toc.py
            │   ├── split_chapters.py
            │   ├── audit_reading_notes.py
            │   └── audit_chapters.py
            └── assets/
                ├── chapter_note_template.md
                ├── book_summary_template.md (deprecated)
                ├── knowledge_card_template.md (deprecated)
                ├── toc_template.md
                └── audit_report_template.md
```

`docs/images/cover.png` 保留在仓库中，但 README 暂不展示封面图。

## 本地测试

```bash
python3 -m unittest discover -s tests
```

CLI smoke test：

```bash
python3 .agents/skills/book-learning/scripts/check_tools.py
python3 .agents/skills/book-learning/scripts/extract_toc.py examples/sample_book.md --out outputs/toc.json
python3 .agents/skills/book-learning/scripts/split_chapters.py examples/sample_book.md --toc outputs/toc.json --out outputs/chapters
python3 .agents/skills/book-learning/scripts/audit_reading_notes.py --toc outputs/toc.json --reading-notes outputs/reading_notes.md --out outputs/audit.json
```

## License

本项目采用 MIT License，详见 [LICENSE](./LICENSE)。

## Contributing

欢迎提交 Issue 和 Pull Request。提交前请运行测试，并确保没有提交任何版权书籍、私人文件或输出目录。

更多说明见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

---

<p align="center">
  <strong>MW · 美未职造</strong><br>
  <a href="https://mollycall.cn">mollycall.cn</a> ·
  <a href="mailto:business@mollycall.cn">business@mollycall.cn</a>
</p>
