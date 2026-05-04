<h1 align="center">book-learning-skill</h1>

<p align="center">
  <strong>From book notes to callable thinking tools.</strong><br>
  <sub>
    By <a href="https://mollycall.cn">MW · 美未职造</a>
    &mdash;
    从读书笔记，到可调用的思维工具
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

**book-learning-skill** is a skill for transforming books into structured notes, method cards, scene triggers, and callable thinking tools for AI agents.

**From book notes to callable thinking tools.**

`book-learning-skill` 是一个面向 AI Agent 的读书与知识调用技能。它不只是把书转成 Markdown 或普通读书笔记，而是进一步把书中的知识归档到用户的 `knowledge_root` / memory palace，提炼成方法卡、场景触发索引和可调用的思维工具，让 Agent 在真实任务中能够主动使用书本知识。

目标不是“读完一本书”，而是让书里的知识真正参与方案评估、商业策划、批判性思考、决策判断、复盘分析和结构化写作。

> 出品：[MW · 美未职造](https://mollycall.cn)  
> License：MIT  
> Status：v4 direction

## 目录

- [项目简介](#项目简介)
- [这个项目解决什么问题](#这个项目解决什么问题)
- [核心理念](#核心理念)
- [How It Works](#how-it-works)
- [Skill](#skill)
- [当前能力](#当前能力)
- [支持格式](#支持格式)
- [输入与输出](#输入与输出)
- [三层输出](#三层输出)
- [快速开始](#快速开始)
- [在 Agent 中使用](#在-agent-中使用)
- [仓库结构](#仓库结构)
- [本地测试](#本地测试)
- [License](#license)
- [Contributing](#contributing)

## 项目简介

`book-learning-skill` 是一个标准 Agent Skill 仓库。它把“学习一本书”拆成一组明确步骤：转换文档、提取目录、拆分章节、逐章提炼、审计遗漏，再产出一份可读、可追溯的完整阅读笔记。阅读笔记完成后，还可以进入第二阶段，把书中的方法提炼为可调用的思维工具。

本仓库只包含 Skill 指令、脚本、模板、测试和自造示例文件；不包含真实书籍、PDF、EPUB、版权摘录或用户私有文件。

## 这个项目解决什么问题

整本书学习不是一个简单摘要任务。长书通常不能一次性塞给模型，普通摘要又很容易跳章、漏细节、丢上下文。很多读书笔记最后只剩结论，却缺少来源追溯，无法确认某个观点来自哪一章、哪些证据或哪些限定条件。

Agent 在处理长文本时需要明确工作流，而不是自由发挥。这个 Skill 将整本书学习拆成可执行步骤，让 Agent 先保留结构，再逐章理解，最后才做跨章整合。

## 核心理念

> 结构保存 > 章节理解 > 干货提炼 > 来源可追溯 > 单一阅读笔记 > 方法卡 > 知识调用

- **结构保存**：先识别目录树和章节边界，再开始总结。
- **章节理解**：每章独立消化，避免只读前几章就生成全书结论。
- **细节保留**：定义、数据、案例、限定条件、反例和反常识观点都不能被粗暴压缩。
- **来源可追溯**：每个观点都应能追溯到章节或行号。
- **干货提炼**：优先提取定义、框架、结论和支撑证据，而不是泛泛分析。
- **单一阅读笔记**：每轮只生成一份 canonical reading notes；有 `knowledge_root` 时直接写入知识库，没有时才写入 `outputs/reading_notes.md`。
- **路径不硬编码**：知识库路径必须来自参数、环境变量、配置文件、Agent 上下文或用户输入。
- **气味索引**：阅读笔记 frontmatter 和 run manifest 都记录 scent tags，供文本索引和可选向量索引使用。
- **知识调用**：阅读笔记完成后，可提炼方法卡、场景索引和调用协议，让书本知识参与真实任务。

## How It Works

```text
User → Agent → book-learning skill
             → raw source → raw Markdown
             → .cache TOC / chapters / audit / manifest
             → canonical reading notes → scent index / index-ready metadata
             → 方法卡 → 场景触发索引 → 知识调用
```

这个流程的关键不是“更快总结”，而是让 Agent 在长文本处理中具备结构感、审计感和可追溯性。

## Skill

| Skill | 描述 | 典型触发词 |
| --- | --- | --- |
| **book-learning** | 系统性学习整本书，完成格式转换、目录提取、逐章阅读、干货提炼、双链回链、阅读笔记审计，并可在第二阶段提炼方法卡和知识调用工具 | `学习这本书` `读一下这本书` `喂你一本书` `逐章做笔记` `整理成阅读笔记` `提炼成方法卡` |

## 当前能力

- [x] 支持 PDF / EPUB / DOCX / HTML / Markdown 工作流
- [x] 将文档统一转换为 Markdown
- [x] 从 Markdown 标题提取目录树
- [x] 输出章节标题、层级、起止行号
- [x] 按目录树拆分章节文件到 `.cache/book-learning/`
- [x] 生成单一 canonical reading notes
- [x] 审计阅读笔记是否覆盖章节、核心字段和双链回链
- [x] 支持 `knowledge_root` / memory palace 归档路径抽象
- [x] 审计知识目录直接子目录并写入 `{matched_knowledge_subdir}`
- [x] 支持 `reading_mode` 路由和模式化审计
- [x] 要求高层视觉区使用 HTML 卡片组件
- [x] 将 scent tags 写入笔记 frontmatter 和 run manifest
- [x] 提供阅读笔记章节模板
- [x] 提供方法卡、场景触发索引、气味向量和调用报告模板
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

- `raw/books/`：原始文件 + 转换后的完整 Markdown，只读保存
- `.cache/book-learning/`：TOC、章节切分、审计报告、运行 manifest
- `outputs/reading_notes.md`：无 `knowledge_root` 时的默认笔记
- `{knowledge_root}/L1-事实与语义/02-📚 知识/`：有 `knowledge_root` 时的唯一笔记输出

主要输出物：

| 输出物 | 说明 |
| --- | --- |
| `raw/books/{book_slug}/{book_slug}.{ext}` | 原始源文件，只读保存 |
| `raw/books/{book_slug}/{book_slug}.md` | 转换后的完整 Markdown，是双链和审计的 source of truth |
| `.cache/book-learning/{book_slug}/toc.json` | 目录树、章节层级、起止行号 |
| `.cache/book-learning/{book_slug}/chapters/` | 章节切分缓存，不是最终产物 |
| `.cache/book-learning/{book_slug}/audit.json` | canonical reading notes 审计报告 |
| `.cache/book-learning/{book_slug}/run_manifest.json` | 给索引、气味路由、可选向量系统读取的入口 |
| `{canonical_notes_path}` | 唯一最终阅读笔记 |

`knowledge_root` 解析优先级：

1. 本次运行显式传入 `--knowledge-root`
2. 环境变量 `BOOK_LEARNING_KNOWLEDGE_ROOT`
3. `.book-learning/config.json` 或 `book-learning.config.json`
4. Agent 上下文中明确约定的 `knowledge_root` / `memory_palace_root`
5. 如果都没有，Agent 会询问是否归档到知识库
6. 用户跳过归档时，fallback 到 `outputs/reading_notes.md`

`canonical_notes_path` 的规则：

```text
有 knowledge_root：{knowledge_root}/L1-事实与语义/02-📚 知识/{matched_knowledge_subdir}/{book_slug}-阅读笔记.md
无 knowledge_root：outputs/reading_notes.md
```

`{matched_knowledge_subdir}` 必须来自知识目录审计、配置、Agent 上下文或用户确认；它不是固定默认值。如果知识目录下有多个子目录且无法高置信匹配，Agent 必须询问：“我发现你的知识目录下有多个子目录，这本书应该归档到哪一个？”

不会保留两份 `reading_notes.md`。如果有 `knowledge_root`，reading notes 直接输出到知识库；`raw` 不保存最终笔记；`chapters/` 是 cache，不是最终产物。开源仓库不会硬编码个人知识库路径。

## 三层输出

### Layer 1: Reading Notes

- 默认输出：`outputs/reading_notes.md`，仅在无 `knowledge_root` 时使用
- 知识库输出：`{knowledge_root}/L1-事实与语义/02-📚 知识/{matched_knowledge_subdir}/{book_slug}-阅读笔记.md`
- 保留原文结构、核心定义、关键框架、核心结论、支撑证据和原文回链
- frontmatter 必须包含 `reading_mode`
- `全书一句话` 和 `全书核心框架` 必须使用内联 HTML 卡片组件
- frontmatter 必须包含 3-5 个有用的 `scent` tags
- 这是基础工作流，不依赖第二阶段

Reading Modes:

- Mode 0：`mode-0-distillation`，教材式干货提炼
- Mode 1：`mode-1-sop`，SOP / 执行手册
- Mode 2：`mode-2-scene-mapping`，场景映射 / 生产力转化
- Mode 3：`mode-3-cognitive-refresh`，认知刷新 / 反常识洞察
- Mode 4：`mode-4-communication-game`，沟通博弈 / 决策推演

如果用户没有指定模式，默认使用 Mode 0；如果 Agent 低置信度，会先询问用户。

### Layer 2: Method Cards

- 从阅读笔记中提炼 3-5 张可执行方法卡
- 每张方法卡都要能用于真实任务
- 方法卡不是章节摘要，也不替代阅读笔记

### Layer 3: Knowledge Invocation

- 场景触发索引
- 气味向量路由
- 方法卡调用协议
- 调用测试样例

Cognitive Toolbox 是第二阶段产物，不影响基础 canonical reading notes 工作流。

## 快速开始

### 方式一：作为 Agent Skill 使用

把本仓库作为项目打开，或将 `.agents/skills/book-learning/` 放入你的 Agent 工作区。

然后对 Agent 说：

> 喂你一本书，帮我逐章学习，并生成一份完整阅读笔记。

Agent 会根据 `.agents/skills/book-learning/SKILL.md` 执行工作流。

如果没有任何 `knowledge_root` 路径约定，Agent 会询问：

> 是否要归档到你的知识库？请提供 knowledge_root 路径。若不提供，将只输出到 outputs/reading_notes.md。

### 方式二：手动运行脚本

```bash
git clone https://github.com/mollycall-zmy/book-learning-skill.git
cd book-learning-skill

python3 -m pip install -r requirements.txt
python3 .agents/skills/book-learning/scripts/check_tools.py
```

使用自造示例书测试：

```bash
mkdir -p raw/books/示例书 .cache/book-learning/示例书
cp examples/sample_book.md raw/books/示例书/示例书.md
python3 .agents/skills/book-learning/scripts/extract_toc.py raw/books/示例书/示例书.md --out .cache/book-learning/示例书/toc.json
python3 .agents/skills/book-learning/scripts/split_chapters.py raw/books/示例书/示例书.md --toc .cache/book-learning/示例书/toc.json --out .cache/book-learning/示例书/chapters
python3 .agents/skills/book-learning/scripts/audit_reading_notes.py --toc .cache/book-learning/示例书/toc.json --reading-notes outputs/reading_notes.md --raw-source raw/books/示例书/示例书.md --out .cache/book-learning/示例书/audit.json
```

使用你自己的 PDF / EPUB / DOCX / HTML：

```bash
python3 .agents/skills/book-learning/scripts/convert_to_md.py path/to/示例书.pdf --out raw/books/{book_slug}/{book_slug}.md
python3 .agents/skills/book-learning/scripts/extract_toc.py raw/books/{book_slug}/{book_slug}.md --out .cache/book-learning/{book_slug}/toc.json
python3 .agents/skills/book-learning/scripts/split_chapters.py raw/books/{book_slug}/{book_slug}.md --toc .cache/book-learning/{book_slug}/toc.json --out .cache/book-learning/{book_slug}/chapters
```

使用知识库归档时，请通过参数、环境变量、配置文件或 Agent 上下文提供 `knowledge_root`。不要把个人本机路径写入仓库文件。

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
- `references/method_card_design.md`
- `references/scene_trigger_index.md`
- `references/scent_vector_routing.md`
- `references/knowledge_invocation.md`
- `scripts/audit_reading_notes.py` 用于审计最终阅读笔记

典型中文触发词：

- 学习这本书
- 读一下这本书
- 喂你一本书
- 帮我逐章消化这个 PDF
- 整理成完整阅读笔记
- 生成可追溯的读书笔记
- 提炼成方法卡
- 生成可调用的思维工具

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
│   ├── cognitive-toolbox/
│   │   ├── README.md
│   │   ├── sample_method_cards.md
│   │   ├── sample_scene_index.md
│   │   └── sample_invocation_tests.md
│   └── sample_book.md
├── tests/
│   ├── test_extract_toc.py
│   ├── test_split_chapters.py
│   ├── test_convert_to_md.py
│   ├── test_audit_reading_notes.py
│   └── test_audit_chapters.py
├── docs/
│   ├── README.md
│   └── images/
│       └── cover.png
├── raw/books/ (git ignored; source assets only)
├── .cache/book-learning/ (git ignored; processing cache)
├── outputs/ (git ignored; default notes only when no knowledge_root exists)
└── .agents/
    └── skills/
        └── book-learning/
            ├── SKILL.md
            ├── references/
            │   ├── workflow.md
            │   ├── method_card_design.md
            │   ├── scene_trigger_index.md
            │   ├── scent_vector_routing.md
            │   ├── knowledge_invocation.md
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
                ├── method_card_template.md
                ├── scene_index_template.md
                ├── scent_vector_template.md
                ├── invocation_report_template.md
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
python3 .agents/skills/book-learning/scripts/extract_toc.py raw/books/示例书/示例书.md --out .cache/book-learning/示例书/toc.json
python3 .agents/skills/book-learning/scripts/split_chapters.py raw/books/示例书/示例书.md --toc .cache/book-learning/示例书/toc.json --out .cache/book-learning/示例书/chapters
python3 .agents/skills/book-learning/scripts/audit_reading_notes.py --toc .cache/book-learning/示例书/toc.json --reading-notes outputs/reading_notes.md --raw-source raw/books/示例书/示例书.md --out .cache/book-learning/示例书/audit.json
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
