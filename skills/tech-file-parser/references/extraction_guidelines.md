# 数据提取详细指南

## 概述

本指南提供从 PDF/Word/Excel 文件中提取技术数据的详细方法，确保数据完整、准确、可追溯。

## 提取原则

### 1. 忠实原文
- 不推断、不假设、不补充
- 只提取文件中明确存在的内容
- 保留原始术语和表达

### 2. 完整性
- 提取数据时包含单位
- 保留测试条件和上下文
- 记录数据来源位置

### 3. 可追溯性
- 每个数据点标注来源
- 页码/Sheet/章节精确到位
- 便于后续核查

### 4. 标记不确定性
- 模糊数据标记 "needs_confirmation"
- OCR 错误可能性高的标记
- 推断的内容明确说明

---

## PDF 文件提取

### 表格提取

**步骤**:
1. 定位表格（通过标题、表号）
2. 识别列头和单位
3. 逐行提取数据
4. 保留表格注释和脚注
5. 记录页码和表号

**示例**:
```json
{
  "table_id": "table_1",
  "source": "report.pdf:Page 12, Table 3",
  "title": "放电容量 vs. 温度",
  "columns": [
    {"name": "Temperature", "unit": "°C"},
    {"name": "Capacity", "unit": "Ah"}
  ],
  "data": [...],
  "notes": "测试条件: 0.2C 放电倍率"
}
```

**常见问题**:
- **合并单元格**: 手动重建结构，标注 parsing_issues
- **跨页表格**: 合并后提取，注明页码范围
- **复杂表头**: 保留层次结构，用嵌套或展平处理

### 图表数据提取

**如果有数据表**: 优先提取表格数据

**如果只有图表**:
1. 描述图表类型（折线/柱状/饼图）
2. 记录坐标轴标签和单位
3. 估算数据点（标注为 approximate）
4. 注明图号和页码
5. 建议从源数据重新生成

**示例**:
```json
{
  "series_id": "series_1",
  "source": "report.pdf:Page 15, Figure 4 (data extracted)",
  "title": "电压 vs. 时间",
  "x_axis": {"name": "Time", "unit": "seconds"},
  "y_axis": {"name": "Voltage", "unit": "V"},
  "notes": "Data estimated from chart, exact values may vary ±2%"
}
```

### 文本中的数据

**提取场景**:
- 规格说明段落
- 测试条件描述
- 结论中的数值

**方法**:
1. 提取数值和单位
2. 保留上下文句子
3. 标注段落或章节
4. 识别关键术语

**示例**:
```json
{
  "claim": "[产品单元]在[极限阈值]下保持87%[性能指标]",
  "source": "report.pdf:Page 5, Section 2.3, Paragraph 2",
  "context": "Conclusions from 100-cycle testing"
}
```

### 扫描 PDF 特殊处理

**挑战**:
- OCR 错误（字符识别错误）
- 表格结构丢失
- 图表无法提取

**策略**:
1. 尝试 OCR 提取
2. 标注 low_confidence
3. 人工核查建议
4. 描述图表内容而非提取数据

---

## Word 文件提取

### 表格提取

**优势**: Word 表格结构清晰，易于解析

**步骤**:
1. 识别表格位置（章节、标题）
2. 提取表头和数据
3. 保留表格样式线索（加粗、颜色）
4. 记录章节和标题层级

**示例**:
```json
{
  "table_id": "table_2",
  "source": "whitepaper.docx:Section 3.2, Table (after heading 'Performance Comparison')",
  "title": "性能对比",
  "columns": [...],
  "data": [...]
}
```

### 列表和项目符号

**提取**:
- 数值列表（规格、要求）
- 步骤列表（流程）
- 对比列表（优缺点）

**转换为结构化数据**:
```json
{
  "list_type": "specifications",
  "source": "whitepaper.docx:Section 2.1, Bullet list",
  "items": [
    {"parameter": "Operating Temp", "value": "-50 to +60", "unit": "°C"},
    {"parameter": "Capacity", "value": "100", "unit": "Ah"}
  ]
}
```

### 段落中的数据

**提取策略**:
1. 识别关键句（包含数值、规格）
2. 提取数值和单位
3. 保留上下文
4. 标注段落位置

**格式化提示**:
- **加粗** = 重要术语或关键数值
- *斜体* = 强调或定义
- 下划线 = 需注意

---

## Excel 文件提取

### 基本原则

**每个 Sheet 单独处理**:
- Sheet 名作为数据集标识
- 记录单元格范围
- 保留 Sheet 之间的关系

### 表格数据提取

**步骤**:
1. 识别表头行（通常第一行）
2. 确定数据范围（有效行列）
3. 提取单元格值
4. 保留单元格注释
5. 处理合并单元格

**示例**:
```json
{
  "table_id": "table_excel_1",
  "source": "test_data.xlsx:Sheet1!A1:D20",
  "title": "测试结果汇总",
  "columns": [
    {"name": "Date", "unit": "YYYY-MM-DD"},
    {"name": "Temperature", "unit": "°C"},
    {"name": "Capacity", "unit": "Ah"}
  ],
  "data": [...],
  "notes": "Data collected from field deployment"
}
```

### 公式处理

**策略**:
- 记录公式内容（如重要）
- 提取计算结果
- 说明计算逻辑

**示例**:
```json
{
  "cell": "D2",
  "formula": "=C2/C1*100",
  "result": 87,
  "description": "Capacity retention percentage"
}
```

### 多 Sheet 关系

**识别**:
- 汇总 Sheet vs. 原始数据 Sheet
- 交叉引用
- 计算依赖

**文档化**:
```json
{
  "sheet_relationships": [
    {
      "sheet": "Summary",
      "references": ["RawData", "Calculations"],
      "description": "Aggregates monthly averages from RawData"
    }
  ]
}
```

### 图表提取

**Excel 图表**:
1. 识别图表类型
2. 定位源数据范围
3. 优先提取源数据表
4. 记录图表标题和轴标签

**示例**:
```json
{
  "chart_id": "chart_1",
  "source": "test_data.xlsx:Sheet2, Chart 1",
  "chart_type": "Line Chart",
  "data_source": "Sheet2!A1:B50",
  "title": "温度 vs. 容量",
  "notes": "Data extracted from source range, chart reconstructible"
}
```

---

## 通用数据模式识别

### 1. 对比数据

**识别特征**:
- "vs.", "compared to", "对比"
- 并列列（Product A, Product B）
- 行标签为参数名

**提取为**:
```json
{
  "comparison_id": "comp_1",
  "title": "产品 A vs. 产品 B",
  "dimensions": [
    {
      "parameter": "Capacity",
      "product_a": "100",
      "product_b": "80",
      "unit": "Ah"
    }
  ]
}
```

### 2. 时间序列

**识别特征**:
- 第一列为日期/时间/周期
- 后续列为测量值
- 趋势性数据

**提取为**:
```json
{
  "time_series_id": "ts_1",
  "x_axis": {"name": "Time", "unit": "hours"},
  "y_axis": {"name": "Voltage", "unit": "V"},
  "data": [
    {"Time": 0, "Voltage": 48.5},
    {"Time": 1, "Voltage": 48.3}
  ]
}
```

### 3. 规格表

**识别特征**:
- 参数名 + 数值 + 单位
- 通常为两列或三列表格
- 标题包含 "Specifications", "Parameters"

**提取为**:
```json
{
  "specifications": [
    {"parameter": "Voltage", "value": "48", "unit": "V"},
    {"parameter": "Capacity", "value": "100", "unit": "Ah"}
  ]
}
```

### 4. 测试结果

**识别特征**:
- 测试条件列 + 结果列
- 通常包含温度、电流等变量
- 重复测试或多次试验

**提取为**:
```json
{
  "test_results": [
    {
      "conditions": {"Temperature": -40, "Current": 20},
      "results": {"Capacity": 87, "Voltage": 47.5}
    }
  ]
}
```

---

## 测试条件提取

### 关键信息

必须提取的测试条件：
1. **温度**: 环境温度、浸泡温度
2. **电流/C-rate**: 充电/放电倍率
3. **时长**: 测试持续时间、循环次数
4. **环境**: 湿度、海拔等（如相关）
5. **设备/标准**: 使用的测试设备或标准

### 提取位置

- 表格标题或注释
- 段落中的描述
- 图表说明
- 文档开头的 "Test Conditions" 章节

### 格式化

```json
{
  "test_conditions": {
    "temperature": {"value": -40, "unit": "°C"},
    "discharge_rate": {"value": 0.2, "unit": "C"},
    "soak_time": {"value": 1, "unit": "hour"},
    "cycles": {"value": 100, "unit": "count"},
    "standard": "IEC 61960-3:2017"
  }
}
```

---

## 可视化机会识别

### 图表类型映射

**折线图** (Line Chart):
- **适用**: 趋势、时间序列、连续变量
- **示例**: 容量 vs. 温度, 电压 vs. 时间
- **优势**: 显示变化趋势

**柱状图** (Bar Chart):
- **适用**: 类别对比、离散数据
- **示例**: 不同产品的容量对比
- **优势**: 清晰的数值对比

**对比表** (Comparison Table):
- **适用**: 多维度参数对比
- **示例**: 规格对比、优缺点对比
- **优势**: 详细信息展示

**饼图** (Pie Chart):
- **适用**: 占比、百分比
- **示例**: TCO 细分、成本构成
- **优势**: 显示整体中的部分

**散点图** (Scatter Plot):
- **适用**: 两个变量关系
- **示例**: 温度 vs. 内阻
- **优势**: 显示相关性

**时间轴** (Timeline):
- **适用**: 项目进度、发展历程
- **示例**: 技术演进、部署计划
- **优势**: 时间维度清晰

**流程图** (Flow Diagram):
- **适用**: 步骤、过程
- **示例**: 测试流程、制造流程
- **优势**: 逻辑关系清晰

### 推荐标准

为每个数据集提供：
1. **图表类型**: 最适合的可视化方式
2. **理由**: 为什么这个类型合适
3. **坐标轴**: X 轴和 Y 轴定义
4. **标题建议**: 清晰的图表标题
5. **标注机会**: 可以高亮的关键点

---

## 质量控制检查清单

### 提取完成后检查

- [ ] 所有表格有来源位置（页/Sheet/章节）
- [ ] 所有数值有单位
- [ ] 测试条件已提取（如有）
- [ ] 列头/参数名清晰
- [ ] 缺失值已标注
- [ ] 不确定数据已标记 needs_confirmation
- [ ] 合并单元格已正确处理
- [ ] 图表数据已提取或描述
- [ ] 跨页/跨 Sheet 数据已合并
- [ ] 公式已描述（如相关）

### JSON 格式检查

- [ ] JSON 语法有效
- [ ] 所有必需字段存在
- [ ] 数据类型正确（数字不要加引号）
- [ ] 嵌套结构正确
- [ ] 数组和对象使用正确

### 可追溯性检查

- [ ] 每个 table_id/series_id 有 source 字段
- [ ] Source 字段格式: `文件名:位置`
- [ ] 位置精确（页码/Sheet/章节）
- [ ] 可以根据 source 快速找到原始数据

---

## 常见错误和解决方案

### 错误 1: 缺少单位
**问题**: 提取数值但忘记单位  
**解决**: 回到原文确认单位，如未明确标注则标记 needs_confirmation

### 错误 2: 过度推断
**问题**: 根据数据推断结论  
**解决**: 只提取明确内容，推断的内容不要包含

### 错误 3: 来源不精确
**问题**: Source 只写 "report.pdf"  
**解决**: 必须包含页码/表号/章节，如 "report.pdf:Page 12, Table 3"

### 错误 4: 忽略测试条件
**问题**: 提取数据但丢失测试条件  
**解决**: 始终提取 test conditions，在 notes 字段中记录

### 错误 5: 复杂表格处理不当
**问题**: 合并单元格、多级表头提取错误  
**解决**: 手动重建结构，标注 parsing_issues 说明

---

## 特殊场景处理

### 场景 1: 多语言文件
- 标注原始语言
- 提取数据（数字通用）
- 保留原始术语
- 术语表中提供翻译（如需要）

### 场景 2: 保密/水印文件
- 提取可见数据
- 标注保密信息位置
- 不推断被遮挡内容

### 场景 3: 版本差异
- 注明文件版本/日期
- 如有多个版本，分别提取
- 标注版本间差异（如发现）

### 场景 4: 不完整文件
- 提取可用部分
- 标注缺失章节/页面
- 在 missing_information 中说明

---

## 输出优化建议

### 1. 数据粒度
- 保留原始粒度（不要过度聚合）
- 如有汇总需求，在 visualization_recommendations 中说明

### 2. 数据结构
- 扁平化 vs. 嵌套: 根据数据复杂度选择
- 数组 vs. 对象: 列表用数组，键值对用对象

### 3. 可读性
- 字段名清晰（英文）
- 值格式统一（数字不加引号）
- 缩进格式化（2 或 4 空格）

### 4. 可机器解析
- JSON 语法严格正确
- 日期格式统一（ISO 8601）
- 单位标准化（SI 单位优先）

---

## 总结

**核心原则**:
1. **忠实原文**: 不推断、不假设
2. **完整性**: 数据 + 单位 + 条件
3. **可追溯**: 精确的来源位置
4. **结构化**: JSON 格式，便于后续使用
5. **标记不确定**: 明确标注需要确认的内容

**质量标准**:
- 所有数据可追溯到源文件
- 所有数值有单位
- 测试条件完整
- 不确定性明确标记
- JSON 格式有效

**最终目标**:
输出的 JSON 可以直接用于:
- 自动生成图表
- 填充文章模板
- 数据验证和审核
- 与研究结果合并

---

*版本: 1.0.0*  
*用途: Tech File Parser Skill 参考指南*
