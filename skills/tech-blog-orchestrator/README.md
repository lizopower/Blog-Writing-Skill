# Technical Blog Orchestrator Skill

## 概述

这是一个**通用的技术/B2B领域**技术博客内容编排 Skill。它作为一个**路由器/编排器**，负责协调研究和文件解析工作流程，并输出结构化的"写作上下文包"（Context Pack）。使用前请先填写下方"行业背景"部分，使其匹配你自己的产品/技术领域。

**重要**: 这个 Skill **不会**生成文章正文、图表或进行 SEO 优化。它的职责是准备和组织信息。

## 行业背景（请替换为你自己的领域）

- **行业**: [你的行业，如"工业设备"]
- **细分市场**: [你的细分市场，如"B2B 极端环境产品定制"]
- **核心优势**: [你的核心差异化优势，如"极端条件下免辅助系统直接运行"]
- **目标受众**: 工程师、采购经理、项目经理

## 使用场景

### 场景1: 仅提供主题
```
用户: "写一篇关于 [产品/技术] 在 [极限条件部署场景] 中应用的技术博客"
```

Skill 会：
1. 识别这是"主题-only"工作流
2. 触发在线研究，收集相关信息
3. 输出包含研究结果的 Context Pack JSON

### 场景2: 仅上传文件
```
用户: [上传 performance_test_data.xlsx, certification_report.pdf]
```

Skill 会：
1. 识别这是"文件-only"工作流
2. 解析所有文件，提取数据和表格
3. 输出包含提取内容的 Context Pack JSON

### 场景3: 主题 + 文件
```
用户: "写一篇关于我们 [产品类别] 在 [极限条件] 下性能优势的博客"
      [上传 performance_comparison.xlsx]
```

Skill 会：
1. 识别这是"主题+文件"工作流
2. **并发**触发研究和文件解析
3. 汇总两路结果，输出完整的 Context Pack JSON

## Context Pack 输出格式

Skill 输出的 JSON 结构包含以下字段：

```json
{
  "topic": "博客主题",
  "audience": ["工程师", "采购经理", "项目经理"],
  "industry_context": {
    "industry": "[你的行业]",
    "market_segment": "[你的细分市场]",
    "core_advantage": "[你的核心差异化优势]"
  },
  "key_claims": [
    {
      "claim": "关键技术或商业声明",
      "source": "来源（URL、文件名+页码）",
      "confidence": "high | medium | low"
    }
  ],
  "extracted_tables": [
    {
      "table_name": "表格名称",
      "source": "来源文件+Sheet/页码",
      "data": "表格数据",
      "description": "表格说明"
    }
  ],
  "glossary": [
    {
      "term": "术语",
      "definition": "定义",
      "context": "为什么这个术语对受众重要"
    }
  ],
  "risk_notes": [
    {
      "issue": "不确定的内容",
      "reason": "为什么标记",
      "recommendation": "建议的人工审核操作"
    }
  ],
  "research_summary": {
    "sources_count": "查阅的来源数量",
    "last_updated": "ISO时间戳",
    "key_findings": ["关键发现列表"]
  },
  "file_summary": {
    "files_processed": ["处理的文件列表"],
    "total_pages": "总页数",
    "extraction_notes": ["提取过程中的注意事项"]
  }
}
```

## 文件结构

```
tech-blog-orchestrator/
├── SKILL.md                              # 主 Skill 定义文件
├── README.md                             # 本文件
├── scripts/
│   └── validate_context_pack.py          # Context Pack 验证脚本
├── references/
│   ├── file_parsing_guide.md             # 文件解析详细指南
│   └── research_strategy.md              # 研究策略详细指南
└── assets/
    └── context_pack_template.json        # Context Pack 模板示例
```

## 核心原则

1. **仅做编排，不生成内容**: 不会写文章正文、不生成图表、不做 SEO
2. **并发执行**: 当主题和文件同时存在时，并行触发研究和解析
3. **来源归属**: 每个 key_claim 必须包含可追溯的来源
4. **风险标记**: 标记任何不确定、矛盾或未验证的信息
5. **结构化输出**: 始终输出有效的 JSON Context Pack

## 验证 Context Pack

使用提供的验证脚本检查 Context Pack 的有效性：

```bash
python scripts/validate_context_pack.py <context_pack.json>
```

脚本会检查：
- 必需字段是否存在
- 数据类型是否正确
- 来源归属是否完整
- JSON 语法是否有效

## 使用建议

1. **明确输入**: 清楚地告诉 AI 你的博客主题或上传相关文件
2. **审核输出**: Context Pack 是设计给人审核的，不要直接用于内容生成
3. **验证来源**: 检查 key_claims 中的来源是否可靠和最新
4. **关注风险**: 重点审查 risk_notes 中标记的不确定内容
5. **灵活调整**: 如果某些信息缺失，可以要求补充研究或提供更多文件

## 扩展性

如果系统中没有专门的 Research 或 Parse Skills，Skill 会降级使用基础工具（如 web_fetch、read_file 等）来完成相同的目标。

## 示例工作流

### 完整示例

**输入**:
```
主题: "[目标场景][极限条件]下的[产品类别]解决方案"
文件: requirements.xlsx, field_test_results.pdf
```

**Skill 执行流程**:
1. ✅ 识别: 主题+文件工作流
2. 🔄 并发触发:
   - 研究: "[deployment scenario] backup requirements", "[extreme-condition] [product category] solutions"
   - 解析: requirements.xlsx 和 field_test_results.pdf
3. 📊 提取数据:
   - 研究: [部署场景]资源需求、市场数据、竞争方案
   - 文件: 需求表格、现场测试数据、性能图表
4. 🔍 质量控制:
   - 验证来源可靠性
   - 标记矛盾数据
   - 构建术语表
5. 📄 输出: 完整的 Context Pack JSON

**输出示例** (简化版):
```json
{
  "topic": "[目标场景][极限条件]下的[产品类别]解决方案",
  "key_claims": [
    {
      "claim": "[部署场景]需要[资源规格]，[N]小时续航",
      "source": "Research: [Standards body] [standard number], 2024-01-15",
      "confidence": "high"
    },
    {
      "claim": "现场测试显示[极限条件]下[性能指标]保持率92%",
      "source": "field_test_results.pdf:p15",
      "confidence": "high"
    }
  ],
  "extracted_tables": [
    {
      "table_name": "不同[条件变量]下的[资源]需求",
      "source": "requirements.xlsx:Sheet1",
      "data": [["[条件变量]", "[资源]", "续航"], ["[极限条件]", "3.2kW", "6h"]]
    }
  ],
  "glossary": [
    {
      "term": "OPEX",
      "definition": "运营支出 - 设备运行和维护的持续成本",
      "context": "[我方方案]通过消除[辅助系统]降低OPEX"
    }
  ]
}
```

## 后续步骤

获得 Context Pack 后，你可以：

1. **人工审核**: 检查所有信息的准确性和完整性
2. **内容创作**: 基于 Context Pack 撰写文章正文（可以请另一个 AI 或人工完成）
3. **视觉设计**: 根据 extracted_tables 创建图表和可视化
4. **SEO 优化**: 基于主题和关键发现进行关键词优化
5. **发布准备**: 最终编辑、格式化和发布

## 技术支持

如需更详细的指导：
- 查看 `references/file_parsing_guide.md` 了解文件解析策略
- 查看 `references/research_strategy.md` 了解研究方法论
- 查看 `assets/context_pack_template.json` 了解完整的输出示例

## 版本信息

- **版本**: 1.0.0
- **创建日期**: 2024-12-26
- **适用行业**: 通用 - 适用于任何技术/B2B领域（替换"行业背景"部分即可）
- **AI 模型要求**: 支持工具调用和并发执行的大语言模型
