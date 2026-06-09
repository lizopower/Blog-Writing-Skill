#!/usr/bin/env python3
"""
Chart Manifest Validator for Tech Visualization Generator

Validates charts_manifest.json structure and data integrity.
Checks for required fields, data traceability, and quality constraints.

Usage:
    python validate_manifest.py <manifest.json>
"""

import json
import sys
import re
from typing import Dict, List, Any, Tuple


class ManifestValidator:
    """Validator for charts_manifest.json"""
    
    REQUIRED_CHART_FIELDS = [
        'chart_id', 'type', 'title', 'data_paths', 'source_ref',
        'metric', 'unit', 'grouping', 'filters', 'assumptions',
        'limitations', 'recommended_size', 'caption', 'alt',
        'data_gaps', 'chart_error'
    ]
    
    VALID_CHART_TYPES = [
        'line_chart', 'bar_chart', 'pie_chart', 'scatter_plot',
        'comparison_table', 'flowchart', 'timeline'
    ]
    
    def __init__(self, manifest_path: str):
        self.manifest_path = manifest_path
        self.manifest = None
        self.errors = []
        self.warnings = []
    
    def load_manifest(self) -> bool:
        """Load and parse manifest JSON"""
        try:
            with open(self.manifest_path, 'r', encoding='utf-8') as f:
                self.manifest = json.load(f)
            return True
        except FileNotFoundError:
            self.errors.append(f"File not found: {self.manifest_path}")
            return False
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {e}")
            return False
    
    def validate_structure(self) -> bool:
        """Validate overall manifest structure"""
        if not isinstance(self.manifest, dict):
            self.errors.append("Manifest must be a JSON object")
            return False
        
        if 'charts_manifest' not in self.manifest:
            self.errors.append("Missing 'charts_manifest' root key")
            return False
        
        manifest = self.manifest['charts_manifest']
        
        # Check required top-level fields
        required_fields = ['total_charts', 'language', 'charts']
        for field in required_fields:
            if field not in manifest:
                self.errors.append(f"Missing required field: {field}")
        
        if 'charts' not in manifest or not isinstance(manifest['charts'], list):
            self.errors.append("'charts' must be a list")
            return False
        
        return len(self.errors) == 0
    
    def validate_chart_ids(self, charts: List[Dict]) -> bool:
        """Validate chart ID format and sequencing"""
        chart_id_pattern = re.compile(r'^chart_\d{2}$')
        
        for i, chart in enumerate(charts):
            chart_id = chart.get('chart_id', '')
            
            # Check format
            if not chart_id_pattern.match(chart_id):
                self.errors.append(
                    f"Chart {i}: Invalid chart_id format '{chart_id}'. "
                    "Must be 'chart_XX' with two digits."
                )
            
            # Check sequence
            expected_id = f"chart_{i+1:02d}"
            if chart_id != expected_id:
                self.warnings.append(
                    f"Chart {i}: chart_id '{chart_id}' breaks sequence. "
                    f"Expected '{expected_id}'."
                )
        
        # Check for duplicates
        chart_ids = [c.get('chart_id') for c in charts]
        duplicates = [id for id in chart_ids if chart_ids.count(id) > 1]
        if duplicates:
            self.errors.append(f"Duplicate chart_ids found: {set(duplicates)}")
        
        return len(self.errors) == 0
    
    def validate_chart(self, chart: Dict, index: int) -> bool:
        """Validate individual chart entry"""
        chart_id = chart.get('chart_id', f'chart_{index}')
        
        # Check required fields
        for field in self.REQUIRED_CHART_FIELDS:
            if field not in chart:
                self.errors.append(f"{chart_id}: Missing required field '{field}'")
        
        # Validate chart type
        chart_type = chart.get('type', '')
        if chart_type not in self.VALID_CHART_TYPES:
            self.errors.append(
                f"{chart_id}: Invalid chart type '{chart_type}'. "
                f"Must be one of: {', '.join(self.VALID_CHART_TYPES)}"
            )
        
        # Validate data_paths
        data_paths = chart.get('data_paths', [])
        if not isinstance(data_paths, list) or len(data_paths) == 0:
            self.errors.append(f"{chart_id}: 'data_paths' must be non-empty list")
        
        # Validate source_ref
        source_ref = chart.get('source_ref', '')
        if not source_ref or source_ref.strip() == '':
            self.errors.append(f"{chart_id}: 'source_ref' cannot be empty")
        elif self._is_generic_source(source_ref):
            self.warnings.append(
                f"{chart_id}: source_ref '{source_ref}' appears generic. "
                "Should include specific page/sheet/section."
            )
        
        # Validate unit (must not be empty for numeric metrics)
        unit = chart.get('unit', '')
        metric = chart.get('metric', '')
        if metric and metric != 'N/A' and not unit:
            self.warnings.append(
                f"{chart_id}: Metric '{metric}' has no unit specified"
            )
        
        # Validate recommended_size
        rec_size = chart.get('recommended_size', {})
        if not isinstance(rec_size, dict):
            self.errors.append(f"{chart_id}: 'recommended_size' must be object")
        elif 'width' not in rec_size or 'aspect_ratio' not in rec_size:
            self.warnings.append(
                f"{chart_id}: 'recommended_size' missing width or aspect_ratio"
            )
        
        # Validate accessibility
        if not chart.get('alt') or chart.get('alt', '').strip() == '':
            self.errors.append(f"{chart_id}: 'alt' text cannot be empty")
        
        if not chart.get('caption') or chart.get('caption', '').strip() == '':
            self.errors.append(f"{chart_id}: 'caption' cannot be empty")
        
        # Validate data_gaps and chart_error
        data_gaps = chart.get('data_gaps', [])
        chart_error = chart.get('chart_error')
        
        if chart_error and chart_error.strip():
            self.warnings.append(
                f"{chart_id}: Has chart_error: '{chart_error}'. "
                "Chart should not be generated."
            )
        
        if data_gaps and len(data_gaps) > 0:
            self.warnings.append(
                f"{chart_id}: Has {len(data_gaps)} data gaps: {data_gaps}"
            )
        
        return True
    
    def _is_generic_source(self, source_ref: str) -> bool:
        """Check if source_ref is too generic"""
        generic_patterns = [
            'industry typical',
            'industry average',
            'common knowledge',
            'general data',
            'typical values'
        ]
        source_lower = source_ref.lower()
        return any(pattern in source_lower for pattern in generic_patterns)
    
    def validate_quality_report(self) -> bool:
        """Validate quality_report section"""
        if 'quality_report' not in self.manifest:
            self.warnings.append("Missing 'quality_report' section")
            return True
        
        report = self.manifest['quality_report']
        charts_count = len(self.manifest['charts_manifest']['charts'])
        
        # Check consistency
        total_generated = report.get('total_charts_generated', 0)
        charts_skipped = report.get('charts_skipped', 0)
        
        if total_generated + charts_skipped != charts_count:
            self.warnings.append(
                f"Quality report counts inconsistent: "
                f"{total_generated} generated + {charts_skipped} skipped "
                f"!= {charts_count} total charts"
            )
        
        # Check for errors
        if report.get('errors', 0) > 0:
            self.warnings.append(
                f"Quality report indicates {report['errors']} errors"
            )
        
        return True
    
    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """Run all validations"""
        if not self.load_manifest():
            return False, self.errors, self.warnings
        
        if not self.validate_structure():
            return False, self.errors, self.warnings
        
        charts = self.manifest['charts_manifest']['charts']
        
        # Validate chart IDs
        self.validate_chart_ids(charts)
        
        # Validate each chart
        for i, chart in enumerate(charts):
            self.validate_chart(chart, i)
        
        # Validate quality report
        self.validate_quality_report()
        
        success = len(self.errors) == 0
        return success, self.errors, self.warnings


def main():
    # Status glyphs (✅/❌/⚠) in the report crash with UnicodeEncodeError on a
    # non-UTF-8 stdout, e.g. a Windows GBK console. Force UTF-8 before printing.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if len(sys.argv) < 2:
        print("Usage: python validate_manifest.py <manifest.json>")
        sys.exit(1)
    
    manifest_path = sys.argv[1]
    
    print(f"Validating manifest: {manifest_path}")
    print("=" * 60)
    
    validator = ManifestValidator(manifest_path)
    success, errors, warnings = validator.validate()
    
    # Print errors
    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
    
    # Print warnings
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")
    
    # Print summary
    print("\n" + "=" * 60)
    if success and not warnings:
        print("✅ VALIDATION PASSED - No errors or warnings")
        sys.exit(0)
    elif success:
        print(f"✅ VALIDATION PASSED - {len(warnings)} warnings")
        sys.exit(0)
    else:
        print(f"❌ VALIDATION FAILED - {len(errors)} errors, {len(warnings)} warnings")
        sys.exit(1)


if __name__ == '__main__':
    main()
