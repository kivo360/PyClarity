#!/usr/bin/env python3
"""
Compare variance between standard and enhanced optimizers
"""

import json
import numpy as np
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def load_metrics(filename="metrics.json"):
    """Load metrics from file"""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def calculate_variance_stats(history):
    """Calculate variance statistics"""
    if not history or len(history) < 2:
        return None
    
    scores = [h["quality_score"] for h in history]
    
    return {
        "mean": np.mean(scores),
        "std": np.std(scores),
        "min": min(scores),
        "max": max(scores),
        "range": max(scores) - min(scores),
        "variance_pct": (np.std(scores) / np.mean(scores) * 100) if np.mean(scores) > 0 else 0
    }

def display_comparison():
    """Display comparison between runs"""
    console.print("\n[bold cyan]Optimizer Variance Comparison[/bold cyan]\n")
    
    # Load current metrics
    metrics = load_metrics()
    if not metrics:
        console.print("[red]No metrics.json found. Run an optimizer first![/red]")
        return
    
    history = metrics.get("history", [])
    current = metrics.get("current", {})
    
    # Calculate stats
    stats = calculate_variance_stats(history)
    
    if not stats:
        console.print("[yellow]Not enough iterations for variance analysis (need at least 2)[/yellow]")
        return
    
    # Display current status
    console.print(Panel(
        f"[bold]Current Iteration:[/bold] {current.get('iteration', 'N/A')}\n"
        f"[bold]Current Score:[/bold] {current.get('quality_score', 0):.1%}\n"
        f"[bold]Total Features:[/bold] {current.get('total_features', 0)}",
        title="Current Status"
    ))
    
    # Create variance table
    table = Table(title="Variance Analysis")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Mean Score", f"{stats['mean']:.1%}")
    table.add_row("Std Deviation", f"{stats['std']:.3f}")
    table.add_row("Score Range", f"{stats['range']:.1%}")
    table.add_row("Min Score", f"{stats['min']:.1%}")
    table.add_row("Max Score", f"{stats['max']:.1%}")
    table.add_row("Variance %", f"{stats['variance_pct']:.1f}%")
    
    console.print(table)
    
    # Show iteration details
    if len(history) > 0:
        console.print("\n[bold]Iteration History:[/bold]")
        for h in history[-5:]:  # Last 5
            strategy = h.get("strategy", {})
            console.print(
                f"  Iter {h['iteration']}: "
                f"{h['quality_score']:.1%} "
                f"({h.get('total_features', 0)} features) "
                f"[dim]{strategy.get('innovation_focus', 'N/A')} | "
                f"{strategy.get('model', 'N/A').split('-')[0]}[/dim]"
            )
    
    # Variance interpretation
    console.print("\n[bold]Variance Interpretation:[/bold]")
    if stats['variance_pct'] < 5:
        console.print("  [red]⚠️  Low variance (<5%) - Consider using enhanced optimizer[/red]")
        console.print("  [dim]Run: ./run_enhanced.sh --reset[/dim]")
    elif stats['variance_pct'] < 10:
        console.print("  [yellow]⚡ Moderate variance (5-10%) - Normal exploration[/yellow]")
    else:
        console.print("  [green]🔥 High variance (>10%) - Good exploration![/green]")

def main():
    """Main entry point"""
    display_comparison()
    
    console.print("\n[dim]Tip: Run this after a few iterations to see variance patterns[/dim]")
    console.print("[dim]For real-time monitoring: watch -n 5 'python compare_variance.py'[/dim]")

if __name__ == "__main__":
    main()