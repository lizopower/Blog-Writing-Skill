# Source Attribution 标准化指南

## 版本
Version: 2.0.0
Last Updated: 2024-12-26

## 目的
统一所有技能中的来源引用格式，确保数据可追溯性和可信度评估。

## 标准格式定义

### 1. PDF 文件

**格式:**
```
filename.pdf:Page XX, Table/Figure/Section X
```

**示例:**
```
performance_test_report.pdf:Page 12, Table 3
performance_test_report.pdf:Page 15, Figure 4
performance_test_report.pdf:Page 8, Section 2.3
```

**必填字段:**
- 文件名 (含扩展名)
- 页码 (Page XX)
- 位置 (Table/Figure/Section + 编号)

---

### 2. Excel 文件

**格式:**
```
filename.xlsx:SheetName!CellRange
```

**示例:**
```
field_data.xlsx:Sheet1!A1:D20
test_results.xlsx:Performance!B5:E50
```

**必填字段:**
- 文件名 (含扩展名)
- Sheet 名称
- 单元格范围 (可选，如果整个 sheet 则省略)

---

### 3. Word 文件

**格式:**
```
filename.docx:Section X.X, Heading 'Title', Paragraph X
```

**示例:**
```
whitepaper.docx:Section 3.2, Heading 'Performance Analysis'
technical_spec.docx:Section 2, Table 1
```

**必填字段:**
- 文件名 (含扩展名)
- Section 编号或 Heading 标题
- 具体位置 (Table/Paragraph 等)

---

### 4. Web 来源

**格式:**
```
URL (Published YYYY-MM-DD, Accessed YYYY-MM-DD)
```

**示例:**
```
https://example.com/research-report (Published 2024-01-15, Accessed 2024-12-26)
```

**必填字段:**
- 完整 URL
- 发布日期 (如果可获取)
- 访问日期

---

### 5. 研究论文

**格式:**
```
Author et al., Journal/Conference, Year
```

**示例:**
```
Zhang et al., Applied Energy, 2023
Li et al., IEEE Transactions on Power Electronics, 2024
```

**必填字段:**
- 第一作者姓氏
- 期刊/会议名称
- 发表年份

---

## 标准化 Source 对象结构

### 完整结构

```json
{
  "source": {
    "type": "pdf" | "excel" | "word" | "web" | "research",
    "reference": "标准格式的引用字符串",
    "url": "file://path 或 https://url (可选)",
    "credibility": "high" | "medium" | "low",
    "verified_by": "技能名称",
    "verified_at": "ISO 8601 时间戳"
  }
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | string | ✅ | 来源类型 |
| reference | string | ✅ | 标准格式引用 |
| url | string | ⭕ | 可点击链接 |
| credibility | string | ✅ | 可信度评级 |
| verified_by | string | ⭕ | 验证者 |
| verified_at | string | ⭕ | 验证时间 |

---

## 可信度评级标准

### High (高可信度)
- 国际标准 (IEC, ISO, GB/T)
- 同行评审期刊论文
- 政府研究机构报告
- 实验室测试报告 (第三方)
- 现场部署数据 (已验证)

### Medium (中等可信度)
- 制造商技术白皮书
- 行业分析报告
- 技术会议论文
- 专利文档
- 行业新闻 (有引用)

### Low (低可信度)
- 公司新闻稿
- 营销材料
- 未验证的用户反馈
- 社交媒体内容
- 无来源的行业传闻

---

## 使用示例

### 示例 1: PDF 测试报告

```json
{
  "claim": "[Product unit] maintains 87% [performance metric] at [extreme threshold]",
  "source": {
    "type": "pdf",
    "reference": "performance_test_report.pdf:Page 12, Table 3",
    "url": "file://c:/data/performance_test_report.pdf#page=12",
    "credibility": "high",
    "verified_by": "tech-file-parser",
    "verified_at": "2024-12-26T10:25:00Z"
  }
}
```

### 示例 2: Excel 现场数据

```json
{
  "claim": "Zero failures over 6-month deployment",
  "source": {
    "type": "excel",
    "reference": "field_data.xlsx:Sheet1!A1:E11",
    "url": "file://c:/data/field_data.xlsx",
    "credibility": "high",
    "verified_by": "tech-file-parser",
    "verified_at": "2024-12-26T10:30:00Z"
  }
}
```

### 示例 3: 研究论文

```json
{
  "claim": "Conventional [product category] requires [auxiliary system] below [moderate threshold]",
  "source": {
    "type": "research",
    "reference": "Li et al., Applied Energy, 2022",
    "url": "https://doi.org/10.1016/j.apenergy.2022.xxxxx",
    "credibility": "high",
    "verified_by": "tech-research",
    "verified_at": "2024-12-26T10:20:00Z"
  }
}
```

---

## 迁移指南

### 从旧格式迁移

**旧格式 (v1.0):**
```json
{
  "claim": "87% capacity at -40°C",
  "source": "test_report.pdf:p.12"
}
```

**新格式 (v2.0):**
```json
{
  "claim": "87% capacity at -40°C",
  "source": {
    "type": "pdf",
    "reference": "test_report.pdf:Page 12, Table 3",
    "credibility": "high"
  }
}
```

### 向后兼容

data-validator 会检测旧格式并提示升级，但不会拒绝旧格式数据。

---

## 验证规则

### 格式验证

1. **PDF**: 必须包含 "Page" 关键字
2. **Excel**: 必须包含 "!" 分隔符
3. **Word**: 必须包含 "Section" 或 "Heading"
4. **Web**: 必须是有效 URL
5. **Research**: 必须包含年份

### 完整性验证

- type 必须是枚举值之一
- reference 不能为空
- credibility 必须是 high/medium/low

---

*此标准适用于所有博客写作技能*
