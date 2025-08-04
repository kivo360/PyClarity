"""PyClarity CLI with MCP server support."""

import asyncio
import typer
from rich import print as rprint
from rich.console import Console

app = typer.Typer(help="PyClarity - Cognitive Tools for Strategic Thinking")
console = Console()


@app.command()
def fire(name: str = "Chell") -> None:
    """Fire portal gun."""
    rprint(f"[bold red]Alert![/bold red] {name} fired [green]portal gun[/green] :boom:")


@app.command()
def server(
    port: int = typer.Option(8000, "--port", "-p", help="Port to run the MCP server on"),
    host: str = typer.Option("localhost", "--host", "-h", help="Host to bind the server to"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode"),
) -> None:
    """Start the PyClarity MCP server."""
    from pyclarity.server.mcp_server import start_server
    
    console.print(f"[bold green]Starting PyClarity MCP Server[/bold green]")
    console.print(f"Host: {host}")
    console.print(f"Port: {port}")
    console.print(f"Debug: {debug}")
    console.print("Available cognitive tools:")
    console.print("  • Mental Models")
    console.print("  • Sequential Thinking") 
    console.print("  • Decision Framework")
    console.print("  • Scientific Method")
    console.print("  • Design Patterns")
    console.print("  • Programming Paradigms")
    console.print("  • Debugging Approaches")
    console.print("  • Visual Reasoning")
    console.print("  • Structured Argumentation")
    console.print("  • Metacognitive Monitoring")
    console.print("  • Collaborative Reasoning")
    console.print("  • Impact Propagation")
    
    try:
        asyncio.run(start_server(host=host, port=port, debug=debug))
    except KeyboardInterrupt:
        console.print("[yellow]Server stopped by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Server error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def list_tools() -> None:
    """List all available cognitive tools."""
    from pyclarity.tools import __all__
    
    console.print("[bold blue]PyClarity Cognitive Tools[/bold blue]")
    console.print("\n[bold]Analyzers:[/bold]")
    
    analyzers = [tool for tool in __all__ if tool.endswith("Analyzer")]
    for analyzer in sorted(analyzers):
        tool_name = analyzer.replace("Analyzer", "").replace("_", " ").title()
        console.print(f"  • {tool_name}")
    
    console.print(f"\n[dim]Total: {len(analyzers)} cognitive tools available[/dim]")


@app.command()
def analyze(
    tool: str = typer.Argument(..., help="Tool name (e.g., 'mental_models')"),
    problem: str = typer.Argument(..., help="Problem to analyze"),
    complexity: str = typer.Option("moderate", "--complexity", "-c", help="Complexity level: simple, moderate, complex"),
) -> None:
    """Analyze a problem using a specific cognitive tool."""
    console.print(f"[bold blue]Analyzing with {tool}[/bold blue]")
    console.print(f"Problem: {problem}")
    console.print(f"Complexity: {complexity}")
    
    # This would integrate with the actual analyzers
    console.print("[yellow]Analysis functionality coming soon![/yellow]")
    console.print("[dim]For now, use the MCP server mode: pyclarity server[/dim]")
