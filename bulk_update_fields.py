#!/usr/bin/env python3
"""
Bulk update Field arguments in Python files:
- Replace max_items with max_length
- Replace min_items with min_length
"""

import os
import re
from pathlib import Path


def update_field_arguments(file_path: Path) -> bool:
    """Update max_items/min_items to max_length/min_length in a file."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Replace max_items with max_length
        content = re.sub(r"\bmax_items\b", "max_length", content)

        # Replace min_items with min_length
        content = re.sub(r"\bmin_items\b", "min_length", content)

        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated: {file_path}")
            return True
        else:
            print(f"No changes needed: {file_path}")
            return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def find_python_files_with_field_args():
    """Find Python files containing max_items or min_items."""
    files_to_update = []

    # Search in src/pyclarity
    src_dir = Path("src/pyclarity")
    if src_dir.exists():
        for py_file in src_dir.rglob("*.py"):
            try:
                with open(py_file, encoding="utf-8") as f:
                    content = f.read()
                    if "max_items" in content or "min_items" in content:
                        files_to_update.append(py_file)
            except Exception as e:
                print(f"Error reading {py_file}: {e}")

    # Search in reward-kit-repo if it exists
    reward_dir = Path("reward-kit-repo")
    if reward_dir.exists():
        for py_file in reward_dir.rglob("*.py"):
            try:
                with open(py_file, encoding="utf-8") as f:
                    content = f.read()
                    if "max_items" in content or "min_items" in content:
                        files_to_update.append(py_file)
            except Exception as e:
                print(f"Error reading {py_file}: {e}")

    return files_to_update


def main():
    """Main function to perform bulk updates."""
    print("Finding Python files with max_items/min_items...")
    files_to_update = find_python_files_with_field_args()

    if not files_to_update:
        print("No files found with max_items or min_items.")
        return

    print(f"\nFound {len(files_to_update)} files to update:")
    for file_path in files_to_update:
        print(f"  - {file_path}")

    print("\nUpdating files...")
    updated_count = 0

    for file_path in files_to_update:
        if update_field_arguments(file_path):
            updated_count += 1

    print(
        f"\nCompleted: {updated_count} files updated out of {len(files_to_update)} files processed."
    )


if __name__ == "__main__":
    main()
