# Blog Writing Skill

A Claude Skills bundle for technical and B2B blog/article production.

## Prerequisites

This bundle requires Tavily for online research. Install Tavily skills first:

```bash
npx skills add https://github.com/tavily-ai/skills
```

Install and authenticate Tavily CLI:

```bash
curl -fsSL https://cli.tavily.com/install.sh | bash
tvly login --api-key tvly-YOUR_KEY
```

Alternative CLI installs:

```bash
uv tool install tavily-cli
# or
pip install tavily-cli
```

You can also authenticate with `tvly login` or `TAVILY_API_KEY`.

Research-dependent skills stop if Tavily is unavailable. They do not silently fall back to generic web search.

## What It Includes

- `blog-brainstorm`: Trellis-like article workspace creation and brief discovery
- `blog-writing-workflow`: end-to-end article workflow with research, validation, strategy pressure test, writing, and fact-checking
- `grill-me`: one-question-at-a-time strategy pressure testing
- `tech-blog-orchestrator`: context pack preparation from topics and files
- `tech-research`: Tavily-backed source research notes
- `tech-file-parser`: structured data extraction from PDF, Word, and Excel files
- `data-validator`: context pack quality checks
- `tech-article-architect`: outline and section planning
- `tech-visualization-generator`: chart manifest generation
- `tech-blog-writer`: final article drafting from outline and context pack
- `fact-checker`: numeric, unit, source, and logic verification
- `content-taste-advisor`: editorial quality and differentiation review

## Article Workspace

The bundle supports Trellis-like article workspaces under:

```text
content/articles/<slug>/
```

See `standards/article_workspace_contract.md` for the full contract.
See `standards/tavily_research_engine.md` for Tavily research requirements.

## Install

Copy this repository folder into your Claude skills directory, or install it using your preferred Claude/Codex skill manager.
