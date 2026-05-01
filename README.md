# book-learning-skill

English version: [README.en.md](README.en.md)

`book-learning-skill` 是一个面向 Codex / Agent 的开源智能体技能，用来把一本书从源文件开始，拆解成可审计、可追溯、可复用的学习成果。它不是“读完后写一段摘要”，而是强调先保留目录结构，再逐章理解，最后产出分层摘要和原子知识卡片。

本仓库只包含 Skill 指令、脚本、模板、测试和自造示例文件；不包含任何真实书籍、PDF、EPUB、版权摘录或用户私有文件。

## 项目简介

这个 Agent Skill 帮助智能体系统化学习整本书。它会把图书转换为 Markdown，提取目录树和行号范围，按章节拆分内容，引导 Agent 逐章做 SQ3R 笔记，并在生成全书总结或知识卡片前执行章节遗漏审计。

适合用于：

- 阅读一本较长的中文或英文书籍
- 从技术书、研究资料、长文档中提取结构化笔记
- 构建个人知识库中的原子知识卡片
- 检查 Agent 是否跳章、漏章或缺少来源依据

## 这个 Skill 解决什么问题

长书学习最容易失败的地方，不是模型不会总结，而是它会太早总结：前几章写得很细，后几章被压缩甚至跳过，最后得到一份看似完整但不可审计的摘要。

本 Skill 把“学习一本书”拆成可验证的步骤：

- 先得到目录树和章节边界
- 再逐章阅读和做笔记
- 再核对章节是否遗漏
- 最后才生成全书摘要和知识卡片

这样可以让输出更稳定，也方便你追溯每个观点来自哪一章。

## 核心理念

- 结构保存优先：先保留目录、层级和章节范围
- 章节理解优先：每章都要有独立笔记
- 细节保留：定义、案例、数据、限定条件、反例都不能随手丢掉
- 来源可追溯：观点必须能回到章节来源
- 分层摘要：从原文到章节笔记，再到全书摘要和知识卡片
- 跨章整合：在完整审计之后再做全书层面的综合
- 原子知识提取：每张卡片只表达一个可复用想法

## 功能特性

- 检测可选转换工具：`pymupdf4llm`、`pandoc`、`ocrmypdf`
- 将 PDF、EPUB、DOCX、HTML、Markdown 统一处理为 Markdown
- 从 Markdown 标题提取 TOC JSON，包含标题、层级、起止行号
- 根据 TOC 拆分章节文件
- 审计目录、章节文件和章节笔记是否遗漏
- 提供章节笔记、全书摘要、知识卡片、TOC、审计报告模板
- 使用标准库 `unittest` 做基础测试，不强制安装测试框架

## 支持的输入格式

MVP 支持以下格式：

| 格式 | 处理方式 | 依赖 |
| --- | --- | --- |
| Markdown | 直接使用或复制 | 无 |
| PDF | 转为 Markdown | `pymupdf4llm` |
| EPUB | 转为 Markdown | `pandoc` 或 `pypandoc_binary` |
| DOCX | 转为 Markdown | `pandoc` 或 `pypandoc_binary` |
| HTML / HTM | 转为 Markdown | `pandoc` 或 `pypandoc_binary` |

扫描版 PDF 需要先做 OCR。v0.1.0 只检测 `ocrmypdf`，不自动执行 OCR 流程。

## 输出物说明

运行时输出默认放在 git 忽略的目录中：

- `raw/books/`：原始书籍文件，只读保存
- `outputs/`：转换后的 Markdown、TOC、章节拆分、笔记和审计报告
- `knowledge_base/`：最终知识卡片和索引

核心输出包括：

- `toc.json`：目录树，包含每个标题的层级和行号范围
- `chapters/*.md`：按 TOC 拆出的章节文件
- `notes/*.notes.md`：逐章 SQ3R 笔记
- `audit.json`：章节遗漏审计结果
- `knowledge_base/cards/*.md`：原子知识卡片

## 工作流程

1. 把原始文件放入 `raw/books/`，并保持只读。
2. 使用 `convert_to_md.py` 将源文件转换为 Markdown。
3. 使用 `extract_toc.py` 提取目录树和行号范围。
4. 使用 `split_chapters.py` 按目录拆分章节。
5. Agent 逐章阅读，按模板生成章节笔记。
6. 使用 `audit_chapters.py` 检查 TOC、章节文件和笔记是否一一对应。
7. 审计通过后，生成全书摘要。
8. 从章节笔记和全书摘要中提取原子知识卡片，并写入知识库。

详细流程见 `.agents/skills/book-learning/references/workflow.md`。

## 仓库结构

```text
book-learning-skill/
├── README.md
├── README.en.md
├── AGENTS.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── examples/
│   └── sample_book.md
├── tests/
│   ├── test_extract_toc.py
│   ├── test_split_chapters.py
│   └── test_audit_chapters.py
└── .agents/
    └── skills/
        └── book-learning/
            ├── SKILL.md
            ├── references/
            ├── scripts/
            └── assets/
```

## 安装依赖

TOC 提取、章节拆分、审计和测试只依赖 Python 标准库。

如果需要处理 PDF、EPUB、DOCX 或 HTML，可以安装可选依赖：

```bash
python3 -m pip install -r requirements.txt
```

外部工具说明：

- PDF：推荐安装 `pymupdf4llm`
- EPUB / DOCX / HTML：推荐安装 `pandoc`
- 如果不想单独安装 pandoc，可尝试 `pypandoc_binary`
- 扫描版 PDF：需要 `ocrmypdf` 及其系统依赖

检查当前环境：

```bash
python3 .agents/skills/book-learning/scripts/check_tools.py
```

v0.1.0 只检测工具，不会自动安装。

## 快速开始

使用仓库内的自造示例书跑一遍完整结构流程：

```bash
python3 .agents/skills/book-learning/scripts/extract_toc.py examples/sample_book.md --out outputs/toc.json
python3 .agents/skills/book-learning/scripts/split_chapters.py examples/sample_book.md --toc outputs/toc.json --out outputs/chapters
python3 .agents/skills/book-learning/scripts/audit_chapters.py --toc outputs/toc.json --chapters outputs/chapters --notes outputs/notes --out outputs/audit.json
```

最后一条命令在没有章节笔记时会返回失败，这是预期行为：它说明章节文件存在，但笔记还没有补齐。

如果要转换文件：

```bash
python3 .agents/skills/book-learning/scripts/convert_to_md.py raw/books/book.pdf --out outputs/book.md
```

## 本地测试

运行基础测试：

```bash
python3 -m unittest discover -s tests
```

测试使用 `examples/sample_book.md`，这是专门为本仓库编写的自造内容，不来自任何真实书籍。

## 如何在 Codex / Agent 中使用

把本仓库作为一个包含 Agent Skill 的项目打开，然后对 Agent 说类似：

- “使用 book-learning 这个 Skill 学习这本书”
- “帮我读完这本书，逐章做笔记，最后生成知识卡片”
- “请先提取目录树，不要直接总结”
- “检查这本书的章节笔记有没有遗漏”

Agent 应当读取 `.agents/skills/book-learning/SKILL.md`，并按其中的顺序执行。长流程、输出格式和卡片规则分别在：

- `.agents/skills/book-learning/references/workflow.md`
- `.agents/skills/book-learning/references/output_schema.md`
- `.agents/skills/book-learning/references/card_rules.md`

## 版权与隐私边界

请不要提交或公开：

- 真实书籍、PDF、EPUB、MOBI、AZW 文件
- OCR 后的整本文本
- 大段版权摘录
- 用户私有文件
- 基于版权书生成的完整知识库

`.gitignore` 已经忽略 `raw/books/`、`outputs/`、`knowledge_base/` 和常见电子书格式。开源仓库只应包含 Skill 指令、脚本、模板、自造示例和测试。

## Roadmap

v0.2.0 计划方向：

- 自动生成章节笔记骨架
- 更稳健的目录识别，支持非标准 Markdown 标题
- 扫描版 PDF 的 OCR 流程编排
- 知识卡片生成脚本和索引更新脚本
- 大型书籍分批处理与断点恢复
- 可选的 Agent UI metadata，例如 `agents/openai.yaml`

## License

MIT License. See [LICENSE](LICENSE).
