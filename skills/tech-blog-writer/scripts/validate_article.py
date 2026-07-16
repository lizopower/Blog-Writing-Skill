#!/usr/bin/env python3
"""
Tech-Blog-Writer Article Validator

Validates final_article.md against quality requirements:
- Numerical governance (sources for all claims)
- Required components (SEO, FAQ, CTA, Self-Audit)
- Style compliance (tone, formatting)
- Structure constraints (≤20 sections)

Usage:
    python validate_article.py path/to/final_article.md
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import json


class ArticleValidator:
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.content = self.filepath.read_text(encoding='utf-8')
        self.errors = []
        self.warnings = []
        self.info = []
        
    def validate(self) -> Dict:
        """Run all validation checks"""
        print(f"Validating: {self.filepath}")
        print("=" * 60)
        
        self.check_front_matter()
        self.check_structure()
        self.check_required_sections()
        self.check_numerical_governance()
        self.check_style_compliance()
        self.check_chart_integration()
        self.check_faq()
        self.check_self_audit()
        
        return self.report()
    
    def check_front_matter(self):
        """Validate YAML front matter"""
        yaml_pattern = r'^---\s*\n(.*?)\n---'
        match = re.search(yaml_pattern, self.content, re.DOTALL)
        
        if not match:
            self.errors.append("Missing YAML front matter")
            return
        
        front_matter = match.group(1)
        
        # Check required fields
        required = ['title', 'description', 'keywords']
        for field in required:
            if f'{field}:' not in front_matter:
                self.errors.append(f"Missing front matter field: {field}")
        
        # Check title length
        title_match = re.search(r'title:\s*(.+)', front_matter)
        if title_match:
            title = title_match.group(1).strip()
            if len(title) > 60:
                self.warnings.append(f"Title too long ({len(title)} chars, max 60)")
            self.info.append(f"Title: {title}")
        
        # Check description length
        desc_match = re.search(r'description:\s*(.+)', front_matter)
        if desc_match:
            desc = desc_match.group(1).strip()
            if len(desc) > 155:
                self.warnings.append(f"Description too long ({len(desc)} chars, max 155)")
            self.info.append(f"Description length: {len(desc)} chars")
    
    def check_structure(self):
        """Validate article structure"""
        # Count H1 headers (should be exactly 1)
        h1_count = len(re.findall(r'^# [^#]', self.content, re.MULTILINE))
        if h1_count == 0:
            self.errors.append("Missing H1 title")
        elif h1_count > 1:
            self.errors.append(f"Multiple H1 titles found ({h1_count}), should be 1")
        else:
            self.info.append(f"✓ H1 count: {h1_count}")
        
        # Count H2 and H3 sections (should be ≤20 total)
        h2_count = len(re.findall(r'^## [^#]', self.content, re.MULTILINE))
        h3_count = len(re.findall(r'^### [^#]', self.content, re.MULTILINE))
        total_sections = h2_count + h3_count
        
        self.info.append(f"H2 sections: {h2_count}")
        self.info.append(f"H3 sections: {h3_count}")
        self.info.append(f"Total sections: {total_sections}")
        
        if total_sections > 20:
            self.warnings.append(f"Too many sections ({total_sections}), recommended ≤20")
        
        # Check for TL;DR section
        if '**TL;DR**' not in self.content and 'TL;DR' not in self.content:
            self.errors.append("Missing TL;DR section")
        else:
            self.info.append("✓ TL;DR section found")
    
    def check_required_sections(self):
        """Check for required article sections"""
        required_sections = {
            'FAQ': r'##\s+FAQ',
            'Self-Audit': r'##\s+Self-Audit Report',
            'CTA': r'##\s+(Next Steps?|Contact|Get |Request |Talk to|Book )',
        }
        
        for name, pattern in required_sections.items():
            if not re.search(pattern, self.content, re.IGNORECASE):
                self.errors.append(f"Missing required section: {name}")
            else:
                self.info.append(f"✓ {name} section found")
    
    def check_numerical_governance(self):
        """Check for quantitative claims without sources"""
        # Pattern to find numbers (percentages, measurements, etc.)
        number_patterns = [
            r'\d+%',  # Percentages
            r'\d+\s*°C',  # Temperatures
            r'\d+\.\d+\s*[A-Za-z]+',  # Measurements with units
            r'\$\d+',  # Costs
            r'\d+\s*cycles',  # Cycle life
            r'\d+-\d+%',  # Ranges
        ]
        
        unsourced_numbers = []
        lines = self.content.split('\n')
        
        for i, line in enumerate(lines):
            # Skip YAML, code blocks, tables, and headers
            if line.startswith('---') or line.startswith('```') or line.startswith('|') or line.startswith('#'):
                continue
            
            for pattern in number_patterns:
                if re.search(pattern, line):
                    # Check if line has source attribution
                    source_patterns = [
                        r'\(PDF p\.\d+',
                        r'\(Sheet:',
                        r'\(Word:',
                        r'\(Source:',
                        r'http[s]?://',
                        r'\[.*\]\(.*\)',  # Markdown link
                    ]
                    
                    # Check current line and next line for source
                    check_lines = [line]
                    if i + 1 < len(lines):
                        check_lines.append(lines[i + 1])
                    
                    has_source = False
                    for check_line in check_lines:
                        for src_pattern in source_patterns:
                            if re.search(src_pattern, check_line):
                                has_source = True
                                break
                        if has_source:
                            break
                    
                    if not has_source and '**Assumption' not in line and 'To Verify' not in line:
                        unsourced_numbers.append((i + 1, line.strip()[:80]))
        
        if unsourced_numbers:
            self.warnings.append(f"Found {len(unsourced_numbers)} potentially unsourced quantitative claims:")
            for line_num, line_text in unsourced_numbers[:5]:  # Show first 5
                self.warnings.append(f"  Line {line_num}: {line_text}...")
            if len(unsourced_numbers) > 5:
                self.warnings.append(f"  ... and {len(unsourced_numbers) - 5} more")
        else:
            self.info.append("✓ No obvious unsourced numbers found")
    
    def check_style_compliance(self):
        """Check for style guideline compliance"""
        # Check for marketing language
        marketing_words = [
            'revolutionary', 'amazing', 'incredible', 'best in class',
            'game-changing', 'breakthrough', 'unparalleled', 'unmatched',
            'leading provider', 'industry leader'
        ]
        
        for word in marketing_words:
            if word.lower() in self.content.lower():
                self.warnings.append(f"Marketing language detected: '{word}'")
        
        # Label lines repealed by writing-plain-language.md
        label_hits = re.findall(
            r'(?im)^\s*\*{0,2}(Key Insight|Non-negotiable|Common Mistake|Trade-off|'
            r'Key takeaway|Bottom line)\*{0,2}\s*:',
            self.content,
        )
        if label_hits:
            self.warnings.append(
                f"Plain-language: label lines still present ({', '.join(sorted(set(label_hits)))}); "
                "fold into complete sentences"
            )
        if re.search(r'(?im)^\s*#{1,3}\s*Ready to\b|Ready to .{0,80}\?', self.content):
            self.warnings.append(
                "Plain-language: 'Ready to…?' CTA/hook detected; use a declarative next-steps heading"
            )

        # Check for overly long paragraphs
        paragraphs = re.split(r'\n\n+', self.content)
        long_paragraphs = []
        
        for i, para in enumerate(paragraphs):
            if para.strip() and not para.startswith('#') and not para.startswith('```'):
                lines = [l for l in para.split('\n') if l.strip() and not l.startswith('-') and not l.startswith('|')]
                if len(lines) > 7:  # More than 7 lines likely too long
                    long_paragraphs.append(i)
        
        if long_paragraphs:
            self.warnings.append(f"Found {len(long_paragraphs)} potentially long paragraphs (>7 lines)")
    
    def check_chart_integration(self):
        """Check chart references and integration"""
        # Find chart references
        chart_refs = re.findall(r'!\[.*?\]\((chart_\d+|chart_TBD_\d+)\)', self.content)
        
        if chart_refs:
            self.info.append(f"Found {len(chart_refs)} chart references: {', '.join(chart_refs)}")
            
            # Check if charts have captions
            for chart_id in chart_refs:
                pattern = rf'!\[.*?\]\({chart_id}\)\s*\n\*Figure \d+:'
                if not re.search(pattern, self.content):
                    self.warnings.append(f"Chart {chart_id} missing caption (Figure X: ...)")
        else:
            self.info.append("No charts referenced in article")
        
        # Check for TBD charts
        tbd_charts = [c for c in chart_refs if 'TBD' in c]
        if tbd_charts:
            self.warnings.append(f"Found {len(tbd_charts)} TBD chart placeholders: {', '.join(tbd_charts)}")
    
    def check_faq(self):
        """Validate FAQ section"""
        faq_section = re.search(r'##\s+FAQ\s*\n(.*?)(?=\n##|\Z)', self.content, re.DOTALL | re.IGNORECASE)
        
        if not faq_section:
            self.errors.append("FAQ section not found")
            return
        
        faq_content = faq_section.group(1)
        
        # Count questions (H3 headers in FAQ section)
        questions = re.findall(r'^###\s+\d+\.', faq_content, re.MULTILINE)
        question_count = len(questions)
        
        if question_count < 6:
            self.errors.append(f"FAQ has {question_count} questions, minimum 6 required")
        else:
            self.info.append(f"✓ FAQ has {question_count} questions")
        
        # Check if answers have sources
        faq_lines = faq_content.split('\n')
        answers_with_sources = 0
        
        for line in faq_lines:
            if '(PDF' in line or '(Sheet:' in line or 'http' in line or '(Source:' in line:
                answers_with_sources += 1
        
        if answers_with_sources == 0 and question_count > 0:
            self.warnings.append("FAQ answers may lack source attribution")
        else:
            self.info.append(f"✓ Found {answers_with_sources} source references in FAQ")
    
    def check_self_audit(self):
        """Validate Self-Audit Report section"""
        audit_section = re.search(r'##\s+Self-Audit Report\s*\n(.*?)(?=\n##|\Z)', self.content, re.DOTALL | re.IGNORECASE)
        
        if not audit_section:
            self.errors.append("Self-Audit Report section not found")
            return
        
        audit_content = audit_section.group(1)
        
        # Check for required subsections
        required_subsections = [
            'High-Risk Statements',
            'Assumptions / To Verify',
            'Data Gaps',
        ]
        
        for subsection in required_subsections:
            if subsection not in audit_content:
                self.errors.append(f"Self-Audit missing subsection: {subsection}")
            else:
                self.info.append(f"✓ Self-Audit includes {subsection}")
        
        # Count items in each subsection
        high_risk_items = len(re.findall(r'^\d+\.\s+\*\*Statement\*\*:', audit_content, re.MULTILINE))
        assumption_items = len(re.findall(r'^\d+\.\s+\*\*Assumption\*\*:', audit_content, re.MULTILINE))
        
        self.info.append(f"Self-Audit: {high_risk_items} high-risk items, {assumption_items} assumptions")
        
        if high_risk_items == 0 and assumption_items == 0:
            self.warnings.append("Self-Audit appears empty (no items found)")
    
    def report(self) -> Dict:
        """Generate validation report"""
        print("\n" + "=" * 60)
        print("VALIDATION REPORT")
        print("=" * 60)
        
        # Errors
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
        else:
            print("\n✅ No critical errors found")
        
        # Warnings
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
        else:
            print("\n✅ No warnings")
        
        # Info
        if self.info:
            print(f"\nℹ️  INFO:")
            for info_item in self.info:
                print(f"  - {info_item}")
        
        # Summary
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        
        status = "PASS" if not self.errors else "FAIL"
        quality = "HIGH" if not self.errors and len(self.warnings) < 5 else "MEDIUM" if not self.errors else "LOW"
        
        print(f"Status: {status}")
        print(f"Quality: {quality}")
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")
        
        return {
            'status': status,
            'quality': quality,
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info,
        }


def main():
    # Status glyphs (✅/❌/✓) in the report crash with UnicodeEncodeError on a
    # non-UTF-8 stdout, e.g. a Windows GBK console. Force UTF-8 before printing.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if len(sys.argv) < 2:
        print("Usage: python validate_article.py path/to/final_article.md")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not Path(filepath).exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    validator = ArticleValidator(filepath)
    result = validator.validate()
    
    # Exit code based on errors
    sys.exit(0 if result['status'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
