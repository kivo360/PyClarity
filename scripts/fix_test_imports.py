#!/usr/bin/env python3
"""
Codemod to fix test import naming mismatches.

This script automatically updates test imports to match the actual class names
in the codebase, fixing plural/singular naming inconsistencies.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Mapping of incorrect names to correct names based on our analysis
IMPORT_FIXES = {
    # Mental Models
    "MentalModelsContext": "MentalModelContext",
    "MentalModelsResult": "MentalModelResult",
    "MentalModelsAnalyzer": "MentalModelsAnalyzer",  # Keep as is
    "FrameworkType": "MentalModelType",  # Changed in newer version
    
    # Scientific Method
    "ScientificMethodContext": "ScientificMethodContext",  # Keep as is
    
    # Decision Framework
    "DecisionFrameworkContext": "DecisionFrameworkContext",  # Keep as is
    
    # Add more mappings as we discover them
}

# Common import patterns to look for
IMPORT_PATTERNS = [
    r"from pyclarity\.tools\.(\w+)\.models import \(([\s\S]*?)\)",
    r"from pyclarity\.tools\.(\w+) import \(([\s\S]*?)\)",
    r"from pyclarity\.tools\.(\w+)\.models import ([\w\s,]+)$",
    r"from pyclarity\.tools\.(\w+) import ([\w\s,]+)$",
]


def fix_imports_in_file(file_path: Path) -> bool:
    """Fix imports in a single file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False
    
    original_content = content
    modified = False
    
    # Apply each fix
    for old_name, new_name in IMPORT_FIXES.items():
        if old_name in content:
            # Fix in import statements
            content = re.sub(
                rf'\b{old_name}\b',
                new_name,
                content
            )
            print(f"  {file_path.name}: {old_name} → {new_name}")
            modified = True
    
    # Special case for MentalModelsFramework -> MentalModelType
    if "MentalModelsFramework" in content:
        content = content.replace("MentalModelsFramework", "MentalModelType")
        print(f"  {file_path.name}: MentalModelsFramework → MentalModelType")
        modified = True
    
    # Write back if modified
    if modified:
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            # Restore original content
            with open(file_path, 'w') as f:
                f.write(original_content)
            return False
    
    return False


def find_additional_mismatches(test_dir: Path) -> Dict[str, List[str]]:
    """Find import mismatches by analyzing test files."""
    mismatches = {}
    
    for test_file in test_dir.rglob("test_*.py"):
        if "__pycache__" in str(test_file):
            continue
            
        try:
            with open(test_file, 'r') as f:
                content = f.read()
        except:
            continue
        
        # Look for imports that might be wrong
        for pattern in IMPORT_PATTERNS:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                tool_name = match.group(1)
                imports = match.group(2)
                
                # Extract individual import names
                import_names = re.findall(r'(\w+)(?:\s*,|\s*\))', imports)
                
                for name in import_names:
                    if "Context" in name or "Result" in name or "Analyzer" in name:
                        if tool_name not in mismatches:
                            mismatches[tool_name] = []
                        if name not in mismatches[tool_name]:
                            mismatches[tool_name].append(name)
    
    return mismatches


def main():
    """Main entry point."""
    project_root = Path(__file__).parent.parent
    test_dir = project_root / "tests"
    
    print("🔧 PyClarity Test Import Fixer")
    print("=" * 50)
    
    # Find potential mismatches
    print("\n📊 Analyzing test imports...")
    mismatches = find_additional_mismatches(test_dir)
    
    print("\n📋 Found imports by tool:")
    for tool, imports in sorted(mismatches.items()):
        print(f"\n{tool}:")
        for imp in sorted(imports):
            print(f"  - {imp}")
    
    # Apply fixes
    print("\n🔨 Applying fixes...")
    fixed_count = 0
    
    for test_file in test_dir.rglob("test_*.py"):
        if "__pycache__" in str(test_file):
            continue
            
        if fix_imports_in_file(test_file):
            fixed_count += 1
    
    print(f"\n✅ Fixed {fixed_count} files")
    
    # Suggest running tests
    print("\n🧪 Next steps:")
    print("1. Run: python -m pytest tests/tools/test_mental_models.py -xvs")
    print("2. If more import errors, add them to IMPORT_FIXES in this script")
    print("3. Run this script again")


if __name__ == "__main__":
    main()