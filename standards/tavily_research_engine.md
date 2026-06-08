# Tavily Research Engine Requirement

Blog-Writing-Skill requires Tavily for online research. Tavily is a hard prerequisite, not an optional enhancement.

## Required Installation

Install Tavily skills:

```bash
npx skills add https://github.com/tavily-ai/skills
```

Install Tavily CLI:

```bash
curl -fsSL https://cli.tavily.com/install.sh | bash
```

Alternative Python installs:

```bash
uv tool install tavily-cli
# or
pip install tavily-cli
```

Authenticate:

```bash
tvly login --api-key tvly-YOUR_KEY
# or
tvly login
# or
export TAVILY_API_KEY=tvly-YOUR_KEY
```

## Preflight

Before running any online research workflow:

1. Confirm Tavily skills are installed or available to the agent.
2. Confirm `tvly` is installed.
3. Confirm authentication via `tvly login` or `TAVILY_API_KEY`.
4. If any check fails, stop and ask the user to install/authenticate Tavily.

Do not silently fall back to generic web search for research tasks.

## Required Research Mapping

- Use `tavily-search` for targeted source discovery.
- Use `tavily-extract` for extracting content from known URLs.
- Use `tavily-research` for deep multi-source reports.
- Use `tavily-map` when finding the right pages on a known site.
- Use `tavily-crawl` when a whole docs/site section must be collected.
- Use `tavily-best-practices` as the implementation and usage reference.

## Blog Workflow Policy

`tech-research` must use Tavily-backed research for online source discovery and extraction.

`tech-blog-orchestrator` must invoke `tech-research` for topic research; `tech-research` is responsible for Tavily usage.

`blog-writing-workflow` must perform Tavily preflight before executing research-dependent steps.

If the user provides only local files and explicitly asks for file parsing without online research, `tech-file-parser` may run without Tavily. Any topic research, source discovery, or claim verification beyond local files still requires Tavily.
