---
version: 1.0.0
title: Reference Corpus Contract
description: Project-local benchmark articles for genre convention extraction only.
---

# Reference Corpus Contract

Benchmark articles live under `content/reference/`. They supply **structure and genre conventions**, not copy-paste source material.

## Layout

```text
content/reference/
├── README.md
└── <topic-slug>/
    └── <article-type>/
        └── *.md
```

Example:

```text
content/reference/
└── industrial-vision/
    ├── case-study/
    │   ├── acme-line-scan.md
    │   └── beta-factory.md
    └── how-to/
        └── calibrate-cameras.md
```

## Rules

1. **No verbatim reuse** in drafts — run `audit_near_duplicate.py` if unsure.
2. Place **3–5** articles per `<topic>/<article-type>` folder when possible; fewer is allowed.
3. Article types align with `article.json.articleType`: `blog`, `how-to`, `case-study`, `comparison`, `white-paper`.
4. Files are project-owned; the bundle does not ship proprietary reference text.

## Extraction

```bash
python skills/tech-article-architect/scripts/extract_genre_conventions.py \
  --root <project-root> \
  --topic industrial-vision \
  --type case-study \
  --slug <article-slug>
```

Writes `content/articles/<slug>/genre_conventions.json` for `tech-article-architect` and `tech-blog-writer`.

## Convention vs fingerprint

| Occurrence across benchmark set | Treatment |
|---------------------------------|-----------|
| ≥3 of 5 articles share a trait | **Genre convention** — recommend in outline/draft |
| 1–2 articles only | **Author style** — optional, do not force |

If a folder has fewer than 3 benchmark articles, extraction may still summarize patterns, but should not force them as genre conventions.
