#!/usr/bin/env python3
"""
Quick validation script for watchexec.

This runs fast checks suitable for continuous monitoring:
watchexec -e py python scripts/quick_validate.py

For comprehensive validation, use validate_references.py
"""
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
CLEAR = "\033[2J\033[H"

def print_header():
    """Print a clear header."""
    print(CLEAR)
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}⚡ Quick Validation | {datetime.now().strftime('%H:%M:%S')}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def run_pyflakes():
    """Run pyflakes for fast undefined name checking."""
    print(f"{YELLOW}🔍 Running pyflakes (fast check)...{RESET}")
    start = time.time()
    
    result = subprocess.run(
        ["pyflakes", "src", "examples"],
        capture_output=True,
        text=True
    )
    
    elapsed = time.time() - start
    
    if result.returncode == 0:
        print(f"{GREEN}✅ No undefined references found ({elapsed:.2f}s){RESET}")
        return True
    else:
        print(f"{RED}❌ Found issues:{RESET}")
        for line in result.stdout.splitlines():
            # Highlight the error type
            if "undefined name" in line:
                print(f"{RED}   ! {line}{RESET}")
            elif "imported but unused" in line:
                print(f"{YELLOW}   ? {line}{RESET}")
            else:
                print(f"   {line}")
        return False

def check_imports():
    """Quick import check for common issues."""
    print(f"\n{YELLOW}🔍 Checking critical imports...{RESET}")
    
    critical_imports = [
        ("pyclarity.db.memory_stores", "MemorySessionStore"),
        ("pyclarity.db.base", "SessionData"),
        ("pyclarity.tools.sequential_thinking.progressive_analyzer", "ProgressiveSequentialThinkingAnalyzer"),
    ]
    
    import_ok = True
    for module, cls in critical_imports:
        try:
            mod = __import__(module, fromlist=[cls])
            if hasattr(mod, cls):
                print(f"{GREEN}   ✓ {cls}{RESET}")
            else:
                print(f"{RED}   ✗ {cls} not found in {module}{RESET}")
                import_ok = False
        except ImportError:
            print(f"{RED}   ✗ Cannot import {module}{RESET}")
            import_ok = False
    
    return import_ok

def check_syntax():
    """Quick syntax check on recently modified files."""
    print(f"\n{YELLOW}🔍 Checking syntax of recent files...{RESET}")
    
    # Find Python files modified in last hour
    src_path = Path("src")
    recent_files = []
    
    for py_file in src_path.rglob("*.py"):
        if py_file.stat().st_mtime > time.time() - 3600:  # Last hour
            recent_files.append(py_file)
    
    if not recent_files:
        print(f"{BLUE}   No recently modified files{RESET}")
        return True
    
    syntax_ok = True
    for file in recent_files[:10]:  # Check up to 10 files
        result = subprocess.run(
            ["python", "-m", "py_compile", str(file)],
            capture_output=True
        )
        if result.returncode == 0:
            print(f"{GREEN}   ✓ {file.relative_to('.')}{RESET}")
        else:
            print(f"{RED}   ✗ {file.relative_to('.')}{RESET}")
            syntax_ok = False
    
    return syntax_ok

def main():
    """Run all quick checks."""
    print_header()
    
    # Track overall status
    all_passed = True
    
    # Run checks
    if not run_pyflakes():
        all_passed = False
    
    if not check_imports():
        all_passed = False
        
    if not check_syntax():
        all_passed = False
    
    # Summary
    print(f"\n{BLUE}{'='*60}{RESET}")
    if all_passed:
        print(f"{GREEN}✅ ALL CHECKS PASSED{RESET}")
        return 0
    else:
        print(f"{RED}❌ SOME CHECKS FAILED{RESET}")
        print(f"{YELLOW}💡 Run 'python scripts/validate_references.py' for detailed analysis{RESET}")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{YELLOW}⚠️  Interrupted{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}💥 Error: {e}{RESET}")
        sys.exit(1)