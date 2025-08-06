"""
Example runner CLI command for PyClarity.

This module provides a CLI command to select and run example files
with memory of the last selection.
"""
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer
from rich import print as rprint
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

# Constants
CACHE_FILE = Path.home() / ".pyclarity" / "last_example.json"
EXAMPLES_DIR = Path(__file__).parent.parent.parent / "examples"

console = Console()


def ensure_cache_dir():
    """Ensure the cache directory exists."""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_last_selection() -> Optional[str]:
    """Load the last selected example file."""
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('last_example')
        except (json.JSONDecodeError, IOError):
            return None
    return None


def save_last_selection(example_path: str):
    """Save the last selected example file."""
    ensure_cache_dir()
    with open(CACHE_FILE, 'w') as f:
        json.dump({'last_example': example_path}, f)


def get_example_files() -> list[Path]:
    """Get all Python files in the examples directory."""
    if not EXAMPLES_DIR.exists():
        return []
    
    # Get all .py files, excluding __pycache__ and hidden files
    examples = []
    for file in EXAMPLES_DIR.rglob("*.py"):
        if "__pycache__" not in str(file) and not file.name.startswith('.'):
            examples.append(file)
    
    return sorted(examples)


def display_examples_table(examples: list[Path]) -> dict[str, Path]:
    """Display examples in a nice table and return a mapping."""
    table = Table(title="Available Examples", show_header=True)
    table.add_column("ID", style="cyan", width=4)
    table.add_column("File", style="green")
    table.add_column("Description", style="dim")
    
    mapping = {}
    
    for idx, example in enumerate(examples, 1):
        # Get relative path from examples dir
        rel_path = example.relative_to(EXAMPLES_DIR)
        
        # Try to extract description from file
        description = ""
        try:
            with open(example, 'r') as f:
                lines = f.readlines()[:10]  # Check first 10 lines
                for line in lines:
                    if line.strip().startswith('"""') or line.strip().startswith("'''"):
                        # Get the docstring
                        if '"""' in line or "'''" in line:
                            # Single line docstring
                            description = line.strip().strip('"""').strip("'''")
                        else:
                            # Multi-line, get next line
                            for next_line in lines[lines.index(line)+1:]:
                                if '"""' in next_line or "'''" in next_line:
                                    break
                                description += next_line.strip() + " "
                        description = description.strip()[:50]
                        if len(description) == 50:
                            description += "..."
                        break
        except:
            pass
        
        if not description:
            description = "No description"
        
        table.add_row(str(idx), str(rel_path), description)
        mapping[str(idx)] = example
        mapping[str(rel_path)] = example
        mapping[example.stem] = example  # Allow selection by filename without extension
    
    console.print(table)
    return mapping


def run_example(example_path: Path, watch: bool = False):
    """Run the selected example file."""
    if not example_path.exists():
        console.print(f"[red]Error: File not found: {example_path}[/red]")
        return
    
    console.print(f"\n[bold blue]Running:[/bold blue] {example_path.relative_to(EXAMPLES_DIR)}")
    console.print("[dim]" + "="*60 + "[/dim]\n")
    
    # Save the selection
    save_last_selection(str(example_path))
    
    # Prepare the command
    cmd = [sys.executable, str(example_path)]
    
    if watch:
        # Use watchexec if available
        watchexec_cmd = ["watchexec", "-e", "py", "--"] + cmd
        
        # Check if watchexec is available
        try:
            subprocess.run(["watchexec", "--version"], capture_output=True, check=True)
            console.print("[yellow]Starting in watch mode (press Ctrl+C to stop)...[/yellow]\n")
            subprocess.run(watchexec_cmd)
        except (subprocess.CalledProcessError, FileNotFoundError):
            console.print("[yellow]watchexec not found, running once...[/yellow]")
            console.print("[dim]Install watchexec for watch mode: brew install watchexec[/dim]\n")
            subprocess.run(cmd)
    else:
        # Run normally
        subprocess.run(cmd)


def examples_command(
    rerun: bool = typer.Option(False, "--rerun", "-r", help="Rerun the last selected example"),
    watch: bool = typer.Option(False, "--watch", "-w", help="Watch for changes and rerun"),
    list_only: bool = typer.Option(False, "--list", "-l", help="List examples without running"),
):
    """
    Run example files interactively.
    
    Select an example file to run from the examples directory.
    Use --rerun to run the last selected example again.
    Use --watch to run with watchexec (auto-restart on changes).
    """
    # Check if examples directory exists
    if not EXAMPLES_DIR.exists():
        console.print(f"[red]Examples directory not found: {EXAMPLES_DIR}[/red]")
        console.print("[yellow]Create an 'examples' directory in your project root.[/yellow]")
        raise typer.Exit(1)
    
    # Get all example files
    examples = get_example_files()
    
    if not examples:
        console.print("[yellow]No example files found in the examples directory.[/yellow]")
        console.print(f"[dim]Looking in: {EXAMPLES_DIR}[/dim]")
        raise typer.Exit(0)
    
    # If list only, just show and exit
    if list_only:
        display_examples_table(examples)
        raise typer.Exit(0)
    
    # Check for rerun
    if rerun:
        last_example = load_last_selection()
        if last_example:
            example_path = Path(last_example)
            if example_path.exists():
                run_example(example_path, watch)
                return
            else:
                console.print(f"[red]Last example no longer exists: {last_example}[/red]")
                console.print("[yellow]Please select a new example.[/yellow]\n")
        else:
            console.print("[yellow]No previous example found. Please select one.[/yellow]\n")
    
    # Display examples and get selection
    console.print("[bold]PyClarity Example Runner[/bold]\n")
    mapping = display_examples_table(examples)
    
    # Get user selection
    console.print("\n[bold]Select an example:[/bold]")
    console.print("[dim]Enter the ID, filename, or relative path[/dim]")
    
    while True:
        selection = Prompt.ask("\nYour choice", default="1")
        
        if selection.lower() in ('q', 'quit', 'exit'):
            console.print("[yellow]Exiting...[/yellow]")
            raise typer.Exit(0)
        
        # Try to find the example
        example_path = mapping.get(selection)
        
        if example_path:
            run_example(example_path, watch)
            break
        else:
            console.print(f"[red]Invalid selection: {selection}[/red]")
            console.print("[dim]Try entering the ID number or filename[/dim]")


# For testing as standalone
if __name__ == "__main__":
    app = typer.Typer()
    app.command()(examples_command)
    app()