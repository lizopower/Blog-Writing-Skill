# Caching Mechanism Guide

## Version
Version: 1.0.0
Last Updated: 2024-12-26

## Purpose
Implement caching to avoid redundant research and file parsing operations.

## Cache Types

### 1. Research Cache
**Location:** `.cache/research/`
**TTL:** 24 hours
**Key Format:** `research_{topic_hash}.json`

**What to Cache:**
- Search results
- Source summaries
- Key claims extracted

**When to Use:**
- Same topic requested within 24 hours
- User explicitly requests cached results

### 2. File Parse Cache
**Location:** `.cache/files/`
**TTL:** Until file changes
**Key Format:** `file_{sha256_hash}.json`

**What to Cache:**
- Extracted tables
- Parsed content
- Metadata

**When to Use:**
- Same file uploaded again
- File hash matches cached version

### 3. Context Pack Cache
**Location:** `.cache/context_packs/`
**TTL:** 7 days
**Key Format:** `cp_{workflow_id}.json`

**What to Cache:**
- Complete Context Pack
- Validation results

**When to Use:**
- User wants to reuse previous research
- Incremental updates to article

## Cache Structure

```json
{
  "cache_key": "research_abc123",
  "created_at": "2024-12-26T10:30:00Z",
  "expires_at": "2024-12-27T10:30:00Z",
  "data": {...},
  "metadata": {
    "skill": "tech-research",
    "version": "1.0.0"
  }
}
```

## Implementation Notes

- Check cache before executing expensive operations
- Validate cache freshness (TTL)
- Clear expired cache automatically
- Provide option to bypass cache

---

*Designed for English content workflow*
