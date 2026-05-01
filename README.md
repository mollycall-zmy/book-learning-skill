<p align="center">
  <img src="docs/images/cover.png" alt="book-learning-skill cover" width="100%">
</p>

<h1 align="center">book-learning-skill</h1>

<p align="center">
  <strong>让 AI Agent 系统性学习整本书的开源技能</strong><br>
  <sub>
    By <a href="https://mollycall.cn">MW · 美未职造</a>
    &mdash;
    结构保存 → 逐章消化 → 审计防漏 → 知识卡片
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

**book-learning-skill** 是一个面向 AI Agent 的开源技能，用来把一本书从 PDF / EPUB / DOCX / HTML 源文件逐步拆解成可审计、可追溯、可复用的结构化知识资产。

它不是“读完写个摘要”，而是围绕目录树、章节笔记、遗漏审计、分层摘要和原子知识卡片，帮助 Agent 更稳地完成整本书学习。

> 出品：[MW · 美未职造](https://mollycall.cn)  
> License：MIT  
> Status：v0.1.x MVP

## 目录

- [这个项目解决什么问题](#这个项目解决什么问题)
- [核心理念](#核心理念)
- [How It Works](#how-it-works)
- [Skill](#skill)
- [功能特性](#功能特性)
- [支持格式](#支持格式)
- [输出物](#输出物)
- [快速开始](#快速开始)
- [本地测试](#本地测试)
- [在 Agent 中使用](#在-agent-中使用)
- [仓库结构](#仓库结构)
- [Roadmap](#roadmap)
- [License](#license--许可证)
- [Brand Notice](#brand-notice--品牌说明)
- [Contributing](#contributing--贡献)

## 这个项目解决什么问题

整本书学习不是一个简单摘要任务。长书通常不能一次性塞给模型，普通摘要又很容易跳章、漏细节、丢上下文。更麻烦的是，很多读书笔记最后只剩结论，却缺少来源追溯，无法确认某个观点来自哪一章、哪些证据或哪些限定条件。

Agent 在处理长文本时需要明确工作流，而不是自由发挥。`book-learning-skill` 把整本书学习拆成可执行步骤：先识别目录树和章节边界，再逐章消化，接着做遗漏审计，最后才生成全书摘要和原子知识卡片。

## 核心理念

> 结构保存 > 章节理解 > 细节保留 > 来源可追溯 > 分层摘要 > 跨章整合 > 原子知识提取

- **结构保存**：先识别目录树和章节边界，再开始总结。
- **章节理解**：每章独立消化，避免只读前几章就生成全书结论。
- **细节保留**：定义、数据、案例、限定条件、反例和反常识观点都不能被粗暴压缩。
- **来源可追溯**：每个观点都应能追溯到章节或行号。
- **分层摘要**：从章节摘录到全书摘要，再到知识卡片，逐层压缩。
- **跨章整合**：在完成逐章笔记后，再做主题归纳和模型提炼。
- **原子知识提取**：每张卡片只保存一个清晰、可复用的想法。

## How It Works

```text
You / User
   │
   ▼
Agent（Codex / Hermes / Cursor / OpenClaw）
   │
   ▼
book-learning-skill
   ├── 检测文件格式
   ├── PDF / EPUB / DOCX / HTML → Markdown
   ├── 提取目录树 + 章节边界
   ├── 按章节拆分内容
   ├── 逐章 SQ3R 阅读与笔记
   ├── 章节遗漏审计
   ├── 分层摘要 L0 → L4
   └── 生成原子知识卡片
   │
   ▼
知识库 / Notes / Atomic Knowledge Cards
```

这个流程的关键不是“更快总结”，而是让 Agent 在长文本处理中具备结构感、审计感和可追溯性。

## Skill

| Skill | 描述 | 典型触发词 |
| --- | --- | --- |
| **book-learning** | 系统性学习整本书，完成格式转换、目录提取、逐章笔记、遗漏审计、分层摘要和原子知识卡片 | `学习这本书` `读一下这本书` `喂你一本书` `逐章做笔记` `把这本书整理成知识卡片` |

## 功能特性

- [x] 支持 PDF / EPUB / DOCX / HTML / Markdown 工作流
- [x] 将文档统一转换为 Markdown
- [x] 从 Markdown 标题提取目录树
- [x] 输出章节标题、层级、起止行号
- [x] 按目录树拆分章节文件
- [x] 检查章节文件与笔记文件是否遗漏
- [x] 提供章节笔记、全书摘要、知识卡片模板
- [x] 提供 Agent Skill 标准目录结构
- [ ] 自动生成章节笔记骨架
- [ ] OCR 流程编排
- [ ] 大型书籍断点续跑
- [ ] 自动生成知识卡片索引

## 支持格式

| 输入格式 | 支持状态 | 处理方式 |
| --- | --- | --- |
| `.md` | 原生支持 | 直接提取目录树和拆章 |
| `.pdf` | 支持 | 使用 PyMuPDF4LLM 转 Markdown |
| `.epub` | 支持 | 使用 Pandoc 转 Markdown |
| `.docx` | 支持 | 使用 Pandoc 转 Markdown |
| `.html` / `.htm` | 支持 | 使用 Pandoc 转 Markdown |
| 扫描版 PDF | 间接支持 | 需先 OCR，再进入 PDF → Markdown 流程 |
| `.caj` / `.nh` / `.kdh` | 暂不直接支持 | 建议先转 PDF，再进入 PDF 工作流 |

## 输出物

这个 Skill 的目标不是只生成一个摘要，而是生成一组可维护的学习资产：

| 输出物 | 说明 |
| --- | --- |
| `toc.json` | 目录树、章节层级、起止行号 |
| `chapters/` | 按章节拆分后的 Markdown 文件 |
| `notes/` | 逐章 SQ3R 笔记 |
| `audit.json` | 章节遗漏审计报告 |
| `book_summary.md` | 全书分层摘要 |
| `knowledge_cards/` | 原子知识卡片 |
| `index.md` | 知识库索引，v0.2.0 计划支持 |

## 快速开始

### 方式一：作为 Agent Skill 使用

把本仓库作为项目打开，或将 `.agents/skills/book-learning/` 放入你的 Agent 工作区。

然后对 Agent 说：

> 喂你一本书，帮我逐章学习，并生成知识卡片。

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

python3 .agents/skills/book-learning/scripts/audit_chapters.py --toc outputs/toc.json --chapters outputs/chapters --notes outputs/notes --out outputs/audit.json
```

使用你自己的 PDF / EPUB / DOCX / HTML：

```bash
python3 .agents/skills/book-learning/scripts/convert_to_md.py path/to/your_book.pdf --out outputs/your_book.md

python3 .agents/skills/book-learning/scripts/extract_toc.py outputs/your_book.md --out outputs/toc.json

python3 .agents/skills/book-learning/scripts/split_chapters.py outputs/your_book.md --toc outputs/toc.json --out outputs/chapters
```

请只使用你合法拥有或有权处理的书籍文件。不要把版权书籍、私人文件或转换后的输出提交到 Git 仓库。

## 本地测试

```bash
python3 -m unittest discover -s tests
```

CLI smoke test：

```bash
python3 .agents/skills/book-learning/scripts/check_tools.py
python3 .agents/skills/book-learning/scripts/extract_toc.py examples/sample_book.md --out outputs/toc.json
python3 .agents/skills/book-learning/scripts/split_chapters.py examples/sample_book.md --toc outputs/toc.json --out outputs/chapters
python3 .agents/skills/book-learning/scripts/audit_chapters.py --toc outputs/toc.json --chapters outputs/chapters --notes outputs/notes --out outputs/audit.json
```

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
- `references/card_rules.md`

典型中文触发词：

- 学习这本书
- 读一下这本书
- 喂你一本书
- 帮我逐章消化这个 PDF
- 把这本书整理成知识卡片
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
            │   └── card_rules.md
            ├── scripts/
            │   ├── check_tools.py
            │   ├── convert_to_md.py
            │   ├── extract_toc.py
            │   ├── split_chapters.py
            │   └── audit_chapters.py
            └── assets/
                ├── chapter_note_template.md
                ├── book_summary_template.md
                ├── knowledge_card_template.md
                ├── toc_template.md
                └── audit_report_template.md
```

`docs/images/cover.png` 是 README 封面图占位路径，当前不会提交图片文件。

## Roadmap

### v0.1.x

- [x] 标准 Agent Skill 目录
- [x] PDF / EPUB / DOCX / HTML / Markdown 转换入口
- [x] TOC 提取
- [x] 章节拆分
- [x] 章节遗漏审计
- [x] 中文 README
- [x] 贡献指南

### v0.2.0

- [ ] `check_tools.py --install` 自动安装可选依赖
- [ ] 自动生成章节笔记骨架
- [ ] `progress.json` 断点续跑
- [ ] OCR 流程编排
- [ ] 自动生成知识卡片索引
- [ ] Obsidian / Logseq 输出适配

### v0.3.0

- [ ] 多本书对比学习
- [ ] 跨章主题聚合
- [ ] 概念图谱
- [ ] 更复杂的目录识别
- [ ] 可视化审计报告

## License / 许可证

This repository is released under the MIT License. See [LICENSE](./LICENSE) for details.

本仓库采用 MIT License 开源，详见 [LICENSE](./LICENSE)。

## Brand Notice / 品牌说明

The source code and general documentation are open under the MIT License.

However, brand assets, cover images, logos, and the “MW · 美未职造” brand identity are not included in the default open-source license unless explicitly stated otherwise.

本仓库中的源代码与通用文档采用 MIT License 开源。

但品牌资产、封面图、Logo，以及 “MW · 美未职造” 品牌标识不默认包含在开源授权范围内；如需用于商业传播、再包装或品牌化复用，请先联系作者。

## Contributing / 贡献

欢迎提交 Issue 和 Pull Request。

适合贡献的方向包括：

- OCR 流程优化
- 自动安装依赖
- 更智能的目录识别
- Obsidian / Logseq 输出格式
- 知识卡片索引
- 多语言 README
- 更多 Agent 平台适配

提交前请确认：

```bash
python3 -m unittest discover -s tests
```

并确保没有提交任何版权书籍、私人文件或输出目录。

更多说明见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

---

<p align="center">
  <strong>MW · 美未职造</strong><br>
  <a href="https://mollycall.cn">mollycall.cn</a> ·
  <a href="mailto:business@mollycall.cn">business@mollycall.cn</a>
</p>
