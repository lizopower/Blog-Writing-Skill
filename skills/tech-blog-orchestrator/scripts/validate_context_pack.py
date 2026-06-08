#!/usr/bin/env python3
"""
Context Pack Validator

Validates that a Context Pack JSON output meets the required schema and quality standards.

Usage:
    python validate_context_pack.py <context_pack.json>
    
Or use as a module:
    from validate_context_pack import validate_context_pack
    result = validate_context_pack(context_pack_data)
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Any, Tuple


def validate_context_pack(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate a Context Pack against the required schema.
    
    Args:
        data: Dictionary containing the Context Pack data
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Required top-level fields
    required_fields = [
        'topic',
        'audience',
        'industry_context',
        'key_claims',
        'extracted_tables',
        'glossary',
        'risk_notes',
        'research_summary',
        'file_summary'
    ]
    
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Validate 'topic'
    if 'topic' in data:
        if not isinstance(data['topic'], str) or not data['topic'].strip():
            errors.append("Field 'topic' must be a non-empty string")
    
    # Validate 'audience'
    if 'audience' in data:
        if not isinstance(data['audience'], list):
            errors.append("Field 'audience' must be a list")
        elif not data['audience']:
            errors.append("Field 'audience' cannot be empty")
    
    # Validate 'industry_context'
    if 'industry_context' in data:
        ic = data['industry_context']
        if not isinstance(ic, dict):
            errors.append("Field 'industry_context' must be an object")
        else:
            required_ic_fields = ['industry', 'market_segment', 'core_advantage']
            for field in required_ic_fields:
                if field not in ic:
                    errors.append(f"Missing field in industry_context: {field}")
    
    # Validate 'key_claims'
    if 'key_claims' in data:
        if not isinstance(data['key_claims'], list):
            errors.append("Field 'key_claims' must be a list")
        else:
            for idx, claim in enumerate(data['key_claims']):
                if not isinstance(claim, dict):
                    errors.append(f"key_claims[{idx}] must be an object")
                    continue
                
                # Check required fields in each claim
                if 'claim' not in claim or not claim['claim']:
                    errors.append(f"key_claims[{idx}] missing 'claim' field")
                if 'source' not in claim or not claim['source']:
                    errors.append(f"key_claims[{idx}] missing 'source' field")
                if 'confidence' in claim:
                    if claim['confidence'] not in ['high', 'medium', 'low']:
                        errors.append(f"key_claims[{idx}] has invalid confidence level")
    
    # Validate 'extracted_tables'
    if 'extracted_tables' in data:
        if not isinstance(data['extracted_tables'], list):
            errors.append("Field 'extracted_tables' must be a list")
        else:
            for idx, table in enumerate(data['extracted_tables']):
                if not isinstance(table, dict):
                    errors.append(f"extracted_tables[{idx}] must be an object")
                    continue
                
                required_table_fields = ['table_name', 'source', 'data']
                for field in required_table_fields:
                    if field not in table:
                        errors.append(f"extracted_tables[{idx}] missing '{field}'")
    
    # Validate 'glossary'
    if 'glossary' in data:
        if not isinstance(data['glossary'], list):
            errors.append("Field 'glossary' must be a list")
        else:
            for idx, term in enumerate(data['glossary']):
                if not isinstance(term, dict):
                    errors.append(f"glossary[{idx}] must be an object")
                    continue
                
                if 'term' not in term or not term['term']:
                    errors.append(f"glossary[{idx}] missing 'term' field")
                if 'definition' not in term or not term['definition']:
                    errors.append(f"glossary[{idx}] missing 'definition' field")
    
    # Validate 'risk_notes'
    if 'risk_notes' in data:
        if not isinstance(data['risk_notes'], list):
            errors.append("Field 'risk_notes' must be a list")
        else:
            for idx, risk in enumerate(data['risk_notes']):
                if not isinstance(risk, dict):
                    errors.append(f"risk_notes[{idx}] must be an object")
                    continue
                
                required_risk_fields = ['issue', 'reason', 'recommendation']
                for field in required_risk_fields:
                    if field not in risk:
                        errors.append(f"risk_notes[{idx}] missing '{field}'")
    
    # Validate 'research_summary'
    if 'research_summary' in data:
        rs = data['research_summary']
        if not isinstance(rs, dict):
            errors.append("Field 'research_summary' must be an object")
        else:
            if 'sources_count' in rs and not isinstance(rs['sources_count'], (int, float)):
                errors.append("research_summary.sources_count must be a number")
            if 'last_updated' in rs:
                try:
                    datetime.fromisoformat(rs['last_updated'].replace('Z', '+00:00'))
                except (ValueError, AttributeError):
                    errors.append("research_summary.last_updated must be valid ISO timestamp")
            if 'key_findings' in rs and not isinstance(rs['key_findings'], list):
                errors.append("research_summary.key_findings must be a list")
    
    # Validate 'file_summary'
    if 'file_summary' in data:
        fs = data['file_summary']
        if not isinstance(fs, dict):
            errors.append("Field 'file_summary' must be an object")
        else:
            if 'files_processed' in fs and not isinstance(fs['files_processed'], list):
                errors.append("file_summary.files_processed must be a list")
            if 'total_pages' in fs and not isinstance(fs['total_pages'], (int, float)):
                errors.append("file_summary.total_pages must be a number")
            if 'extraction_notes' in fs and not isinstance(fs['extraction_notes'], list):
                errors.append("file_summary.extraction_notes must be a list")
    
    # Quality checks
    if 'key_claims' in data and isinstance(data['key_claims'], list):
        if len(data['key_claims']) == 0:
            errors.append("QUALITY WARNING: No key_claims provided (expected at least 1)")
    
    if 'research_summary' in data and isinstance(data['research_summary'], dict):
        if data['research_summary'].get('sources_count', 0) == 0:
            if 'file_summary' not in data or len(data['file_summary'].get('files_processed', [])) == 0:
                errors.append("QUALITY WARNING: No research sources and no files processed")
    
    is_valid = len(errors) == 0
    return is_valid, errors


def validate_from_file(file_path: str) -> Tuple[bool, List[str]]:
    """
    Validate a Context Pack from a JSON file.
    
    Args:
        file_path: Path to JSON file containing Context Pack
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return validate_context_pack(data)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {str(e)}"]
    except FileNotFoundError:
        return False, [f"File not found: {file_path}"]
    except Exception as e:
        return False, [f"Error reading file: {str(e)}"]


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_context_pack.py <context_pack.json>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    is_valid, errors = validate_from_file(file_path)
    
    if is_valid:
        print("✅ Context Pack is VALID")
        sys.exit(0)
    else:
        print("❌ Context Pack is INVALID")
        print(f"\nFound {len(errors)} error(s):")
        for idx, error in enumerate(errors, 1):
            print(f"  {idx}. {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
