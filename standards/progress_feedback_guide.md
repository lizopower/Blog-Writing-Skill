# Progress Feedback System Guide

## Version
Version: 1.0.0
Last Updated: 2024-12-26

## Purpose
Provide real-time progress feedback during blog writing workflow execution to improve user experience.

## Progress Display Format

### Standard Format

```
Step X/Y: [Step Name] ([Skill Name])
├─ [████████░░] 80% [Current Action]
├─ [Status Info]
└─ Estimated Time Remaining: XXs
```

### Example Output

```
Step 1/4: Content Preparation (tech-blog-orchestrator)
├─ [████████░░] 80% Researching topic...
├─ Found 12 relevant sources
└─ Estimated Time Remaining: 30s

Step 2/4: Article Architecture (tech-article-architect)
├─ [██████████] 100% Complete
├─ Generated 18 sections
└─ Duration: 15s

Step 3/4: Visualization (tech-visualization-generator)
├─ [██████░░░░] 60% Generating charts...
├─ Generated 3/5 charts
└─ Estimated Time Remaining: 20s

Step 4/4: Article Writing (tech-blog-writer)
├─ [░░░░░░░░░░] 0% Waiting...
```

## Implementation Guidelines

### For blog-writing-workflow

Add progress tracking at each step:

1. Before calling sub-skill → Display "Starting..."
2. During execution → Update progress percentage
3. After completion → Display "Complete" + duration

