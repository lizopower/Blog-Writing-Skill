# File Parsing Guide for Technical Blog Orchestrator

## Overview

This reference provides detailed instructions for parsing different file types when orchestrating technical blog content. Use this guide when files are uploaded as part of the blog writing workflow.

## Supported File Types

### PDF Files (.pdf)

**Primary Goals**:
- Extract text content with page number references
- Identify and extract tables
- Preserve technical specifications and data
- Flag any images or charts that cannot be extracted as text

**Extraction Strategy**:
1. Use appropriate PDF parsing tools (e.g., PyPDF2, pdfplumber, or built-in tools)
2. Extract text page-by-page to maintain page number references
3. Identify tabular data structures and extract as structured data
4. Note any figures, charts, or images with their captions and page numbers
5. Preserve technical terms, units, and specifications exactly as written

**Output Format**:
```json
{
  "file_name": "report.pdf",
  "total_pages": 25,
  "extracted_text": {
    "page_1": "Full text content...",
    "page_2": "Full text content..."
  },
  "tables": [
    {
      "page": 5,
      "table_name": "Performance Comparison",
      "data": [[row1], [row2]],
      "headers": ["Column1", "Column2"]
    }
  ],
  "figures": [
    {
      "page": 8,
      "caption": "[Performance metric] curve at [extreme threshold]",
      "type": "chart"
    }
  ]
}
```

### Excel Files (.xlsx, .xls)

**Primary Goals**:
- Extract data from all sheets
- Preserve sheet names and structure
- Identify headers and data types
- Extract any embedded charts metadata (not the visual, just description)

**Extraction Strategy**:
1. Use appropriate Excel parsing tools (e.g., openpyxl, pandas, or built-in tools)
2. Iterate through all sheets in the workbook
3. For each sheet, identify header rows and data rows
4. Extract formulas as values (calculated results)
5. Note any merged cells, comments, or special formatting

**Output Format**:
```json
{
  "file_name": "performance_data.xlsx",
  "sheets": [
    {
      "sheet_name": "Test Results",
      "row_count": 150,
      "column_count": 8,
      "headers": ["Temperature", "Voltage", "Current", "Capacity"],
      "data": [[row1_data], [row2_data]],
      "summary_stats": {
        "numeric_columns": ["Temperature", "Voltage"],
        "min_max": {"Temperature": [-60, 25]}
      }
    }
  ],
  "embedded_charts": [
    {
      "sheet": "Test Results",
      "chart_type": "line",
      "description": "Voltage vs. Temperature"
    }
  ]
}
```

### Word Documents (.docx)

**Primary Goals**:
- Extract structured text content
- Identify headings and document structure
- Extract tables with formatting
- Preserve lists, bullet points, and numbering

**Extraction Strategy**:
1. Use appropriate Word parsing tools (e.g., python-docx or built-in tools)
2. Extract content while preserving paragraph styles and heading levels
3. Identify and extract tables with proper structure
4. Note any embedded images with their alt text or captions
5. Preserve document metadata (author, date, version if available)

**Output Format**:
```json
{
  "file_name": "product_spec.docx",
  "metadata": {
    "author": "Engineering Team",
    "created": "2024-01-15",
    "modified": "2024-03-20"
  },
  "structure": [
    {
      "type": "heading",
      "level": 1,
      "text": "Product Overview"
    },
    {
      "type": "paragraph",
      "text": "Full paragraph content..."
    },
    {
      "type": "table",
      "rows": 5,
      "columns": 3,
      "data": [[row1], [row2]]
    }
  ]
}
```

## Common Parsing Challenges

### Challenge 1: Unstructured Tables in PDFs
**Issue**: Tables in PDFs may not have clear borders or structure
**Solution**: 
- Use heuristic analysis to identify aligned text as columns
- Flag uncertain extractions in risk_notes
- Recommend human verification for critical data

### Challenge 2: Complex Excel Formulas
**Issue**: Some cells contain formulas that reference other sheets
**Solution**:
- Extract calculated values, not formula text
- Note if circular references or errors exist
- Flag any #N/A, #REF!, or #DIV/0! errors

### Challenge 3: Mixed Language Content
**Issue**: Files may contain Chinese and English text
**Solution**:
- Preserve original language for technical terms
- Note language mix in file_summary
- Extract glossary terms in both languages if present

### Challenge 4: Large Files
**Issue**: Files may be very large (100+ pages, 10k+ rows)
**Solution**:
- Prioritize extraction of summary data, tables, and key sections
- Sample data if necessary (e.g., first 1000 rows)
- Note in extraction_notes if content was sampled

## Quality Checks

Before finalizing parsed content, perform these checks:

1. **Completeness**: Verify all sheets/pages were processed
2. **Data Integrity**: Check for obvious errors (negative timestamps, impossible values)
3. **Source Attribution**: Ensure every extracted piece has page/sheet reference
4. **Technical Accuracy**: Preserve units, decimals, and significant figures
5. **Risk Flagging**: Identify and flag any uncertain or ambiguous extractions

## Integration with Context Pack

Map parsed file data to Context Pack fields:

- **extracted_tables**: All tables from all files with source metadata
- **key_claims**: Any explicit claims or conclusions in the files
- **glossary**: Technical terms found in the files with context
- **risk_notes**: Any extraction uncertainties or data quality issues
- **file_summary**: Overview of what was processed and any issues

## Example: Multi-File Processing

When processing multiple files:

```python
# Pseudo-code workflow
files = [performance_test.xlsx, certification.pdf, spec_sheet.docx]
all_tables = []
all_claims = []
all_terms = {}
all_risks = []

for file in files:
    parsed = parse_file(file)  # Use appropriate parser
    all_tables.extend(parsed.tables)
    all_claims.extend(parsed.claims)
    all_terms.update(parsed.glossary)
    all_risks.extend(parsed.risks)

context_pack = {
    "extracted_tables": all_tables,
    "key_claims": all_claims,
    "glossary": all_terms,
    "risk_notes": all_risks,
    "file_summary": {
        "files_processed": [f.name for f in files],
        "total_pages": sum_pages(files)
    }
}
```

## Tools and Libraries Reference

Recommended tools for file parsing:

- **PDF**: pdfplumber, PyPDF2, pdf tool skill
- **Excel**: openpyxl, pandas, xlsx skill
- **Word**: python-docx, docx skill

Always prefer using dedicated skills if available for better reliability.
