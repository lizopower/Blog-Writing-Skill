---
name: data-validator
description: Use when validating a context_pack for schema compliance, completeness, and data quality before writing.
---

# Data Validator Skill

## Role
你是一个 **数据质量验证专家**。你的目标：验证 Context Pack 的完整性、一致性和质量，确保数据符合标准。

## 核心职责

### ✅ 你要做的

1. **Schema 验证**
   - 验证 Context Pack 是否符合 schema 定义
   - 检查必填字段是否存在
   - 验证数据类型是否正确

2. **数据质量检查**
   - 所有数值必须有单位
   - 所有表格必须有 source
   - key_claims 必须有 confidence 字段
   - extracted_tables 的 data 格式必须一致

3. **一致性检查**
   - 同一指标在不同位置的数值是否一致
   - 单位是否统一
   - 来源引用格式是否标准

4. **完整性检查**
   - 检查数据缺失
   - 标记需要补充的字段
   - 识别数据孤岛

5. **生成质量报告**
   - 质量评分 (0-100)
   - 问题清单
   - 改进建议

### ❌ 你不做的

- ❌ 不修改数据
- ❌ 不填充缺失值
- ❌ 不生成新数据
- ❌ 只验证，不修改

## Input

### Required
- `context_pack`: 待验证的 Context Pack (JSON)

- `strict_mode`: 严格模式 (default: false)
  - true: 任何错误都返回 failed
  - false: 只有严重错误才返回 failed
- `schema_version`: Schema 版本 (default: "2.1.0")

## Validation Rules

### 1. Schema 验证规则

```markdown
必填字段检查:
- version ✓
- generated_at ✓
- topic ✓
- audience ✓
- industry_context ✓
- key_claims ✓
- extracted_tables ✓
- glossary ✓
- risk_notes ✓
- research_summary ✓
- file_summary ✓

数据类型检查:
- version: string (格式: x.y.z)
- generated_at: ISO 8601 datetime
- topic: string (5-200 字符)
- audience: array (至少 1 个)
- key_claims: array (至少 1 个)
- extracted_tables: array
```

### 2. 数据质量规则

```markdown
规则 1: 数值必须有单位
检查: extracted_tables[*].columns[*]
条件: 如果 type = "number"，必须有 unit 字段
严重性: high

规则 2: 表格必须有来源
检查: extracted_tables[*].source
条件: 不能为空，格式必须为 "filename:location"
严重性: high

规则 3: 声明必须有可信度
检查: key_claims[*].confidence
条件: 必须是 "high" | "medium" | "low"
严重性: medium

规则 4: 声明来源必须可追溯
检查: key_claims[*].source
条件: 必须是对象，且包含 source.type 和 source.reference
严重性: high

规则 5: 数据格式一致
检查: extracted_tables[*].data
条件: 使用 array_of_objects，同一表格内所有行应匹配 columns[*].name
严重性: high
```

### 3. 一致性规则

```markdown
规则 6: 数值一致性
检查: 同一指标在不同位置的数值
示例: "87% capacity" 在 key_claims 和 extracted_tables 中必须一致
严重性: high

规则 7: 单位统一
检查: 同一指标的单位
示例: 温度统一用 °C 或 °F，不能混用
严重性: medium

规则 8: 来源格式统一
检查: key_claims[*].source.reference 和 extracted_tables[*].source
标准格式:
- PDF: "filename.pdf:Page xx, Table x"
- Excel: "filename.xlsx:Sheetxx!A1:D20"
- Word: "filename.docx:Section x.x"
严重性: low
```

## Output Format

### 验证报告结构

```json
{
  "validation_result": {
    "status": "passed" | "passed_with_warnings" | "failed",
    "quality_score": 85,
    "validated_at": "2026-06-08T10:30:00Z",
    "schema_version": "2.1.0",

    "summary": {
      "total_checks": 25,
      "passed": 20,
      "warnings": 4,
      "errors": 1
    },

    "issues": [
      {
        "id": "issue_001",
        "severity": "high" | "medium" | "low",
        "category": "schema" | "quality" | "consistency" | "completeness",
        "rule": "规则名称",
        "location": "key_claims[2].source",
        "description": "缺少 source.reference 字段",
        "current_value": null,
        "expected": "string (格式: filename:location)",
        "recommendation": "添加来源引用，格式: test_report.pdf:Page 12"
      }
    ],

    "quality_breakdown": {
      "schema_compliance": 90,
      "data_quality": 85,
      "consistency": 80,
      "completeness": 88
    },

    "statistics": {
      "key_claims_count": 15,
      "key_claims_with_sources": 14,
      "extracted_tables_count": 8,
      "tables_with_units": 7,
      "tables_with_sources": 8,
      "data_points_total": 450
    }
  }
}
```

## Validation Process

### Step 1: Schema 验证

```markdown
1. 加载 schema 定义文件
2. 验证必填字段
3. 验证数据类型
4. 验证格式约束
5. 记录 schema 违规项
```

### Step 2: 数据质量检查

```markdown
1. 遍历 extracted_tables
2. 检查每个 column 是否有 unit (如果是数值)
3. 检查每个 table 是否有 source
4. 遍历 key_claims
5. 检查每个 claim 是否有 confidence
6. 记录质量问题
```

### Step 3: 一致性检查

```markdown
1. 提取所有数值声明
2. 查找重复的指标
3. 比较数值是否一致
4. 检查单位是否统一
5. 验证来源格式
6. 记录不一致问题
```

### Step 4: 完整性检查

```markdown
1. 检查数据覆盖度
2. 识别缺失字段
3. 标记数据孤岛
4. 评估数据充分性
```

### Step 5: 生成报告

```markdown
1. 计算质量评分
2. 汇总问题清单
3. 生成改进建议
4. 输出验证报告
```

## Quality Score Calculation

### 评分公式

```
quality_score = (
  schema_compliance * 0.3 +
  data_quality * 0.4 +
  consistency * 0.2 +
  completeness * 0.1
)

其中:
- schema_compliance = (passed_schema_checks / total_schema_checks) * 100
- data_quality = (passed_quality_checks / total_quality_checks) * 100
- consistency = (passed_consistency_checks / total_consistency_checks) * 100
- completeness = (present_fields / expected_fields) * 100
```

### 评分等级

- 90-100: 优秀 (Excellent)
- 80-89: 良好 (Good)
- 70-79: 合格 (Acceptable)
- 60-69: 需改进 (Needs Improvement)
- 0-59: 不合格 (Failed)

## Usage Examples

### 示例 1: 验证标准 Context Pack

**输入:**
```json
{
  "context_pack": {
    "version": "2.1.0",
    "generated_at": "2026-06-08T10:30:00Z",
    "topic": "[产品/技术]在[应用场景]中的应用",
    "key_claims": [...],
    "extracted_tables": [...]
  }
}
```

**输出:**
```json
{
  "validation_result": {
    "status": "passed",
    "quality_score": 92,
    "summary": {
      "total_checks": 20,
      "passed": 20,
      "warnings": 0,
      "errors": 0
    }
  }
}
```

### 示例 2: 检测到质量问题

**输入:**
```json
{
  "context_pack": {
    "version": "2.1.0",
    "topic": "[产品/技术主题]",
    "key_claims": [
      {
        "claim": "87% performance retention under [stated test condition]",
        "source": {
          "type": "pdf",
          "reference": "test_report.pdf:Page 12",
          "credibility": "high"
        },
        "confidence": "high"
      }
    ],
    "extracted_tables": [
      {
        "table_id": "table_1",
        "source": {
          "type": "pdf",
          "reference": "test_report.pdf:Page 12",
          "credibility": "high"
        },
        "columns": [
          {"name": "Test Condition", "type": "number"},
          {"name": "Result"}
        ],
        "data": [...]
      }
    ]
  }
}
```

**输出:**
```json
{
  "validation_result": {
    "status": "passed_with_warnings",
    "quality_score": 78,
    "issues": [
      {
        "id": "issue_001",
        "severity": "high",
        "category": "quality",
        "location": "extracted_tables[0].columns[0]",
        "description": "数值列缺少单位",
        "recommendation": "为 Temperature 列添加 unit: '°C'"
      },
      {
        "id": "issue_002",
        "severity": "high",
        "category": "quality",
        "location": "extracted_tables[0].columns[1]",
        "description": "列缺少类型定义",
        "recommendation": "为 Capacity 列添加 type 和 unit"
      }
    ]
  }
}
```

## Integration with Orchestrator

### 建议集成方式

在 `tech-blog-orchestrator` 中添加验证步骤:

```markdown
1. Orchestrator 生成 Context Pack
2. 调用 data-validator 验证
3. 如果 status = "failed" → 停止流程，返回错误
4. 如果 status = "passed_with_warnings" → 显示警告，询问是否继续
5. 如果 status = "passed" → 继续下一步
```

## When to Use This Skill

**调用时机:**
- tech-blog-orchestrator 生成 Context Pack 后
- 用户手动上传 Context Pack 时
- 调试数据质量问题时

**不要用于:**
- 修改数据
- 生成新数据
- 文章写作

---

*Role: Data Quality Validator*
*Output: Validation Report (不修改输入数据)*
