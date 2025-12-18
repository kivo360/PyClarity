"""PyClarity CLI with MCP server support."""

import asyncio

import typer
from fastmcp import FastMCP
from rich import print as rprint
from rich.console import Console

from pyclarity.config import MCPConfig
from pyclarity.server.mcp_server import PyClarityMCPServer
from pyclarity.cli_examples import examples_command

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
    transport: str = typer.Option(
        "streamable-http",
        "--transport",
        "-t",
        help="Transport to use for the server (http, streamable-http, stdio)",
    ),
) -> None:
    """Start the PyClarity MCP server."""

    console.print("[bold green]Starting PyClarity MCP Server[/bold green]")
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
        # Create and start the MCP server
        config = MCPConfig()
        config.server.host = host
        config.server.port = port
        config.server.debug = debug

        server = PyClarityMCPServer(config)

        console.print("[bold green]Starting PyClarity MCP Server[/bold green]")
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

        # Start the server
        asyncio.run(server.start(host=host, port=port))

    except KeyboardInterrupt:
        console.print("[yellow]Server stopped by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Server error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def list_tools() -> None:
    """List all available cognitive tools."""
    try:
        server = PyClarityMCPServer()
        tools = server.tools.tools
        
        console.print("[bold blue]PyClarity Cognitive Tools[/bold blue]")
        console.print("\n[bold]Analyzers:[/bold]")
        
        for tool_name, tool in sorted(tools.items()):
            # Format tool name nicely
            display_name = tool_name.replace("_", " ").title()
            description = getattr(tool, 'description', 'No description available')
            console.print(f"  • [bold]{display_name}[/bold]: {description}")
        
        console.print(f"\n[dim]Total: {len(tools)} cognitive tools available[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error loading tools: {e}[/red]")
        console.print("[dim]Total: 0 cognitive tools available[/dim]")


@app.command()
def analyze(
    tool: str = typer.Argument(..., help="Tool name (e.g., 'mental_models')"),
    problem: str = typer.Argument(..., help="Problem to analyze"),
    complexity: str = typer.Option(
        "moderate", "--complexity", "-c", help="Complexity level: simple, moderate, complex"
    ),
) -> None:
    """Analyze a problem using a specific cognitive tool."""
    console.print(f"[bold blue]Analyzing with {tool}[/bold blue]")
    console.print(f"Problem: {problem}")
    console.print(f"Complexity: {complexity}")

    # This would integrate with the actual analyzers
    console.print("[yellow]Analysis functionality coming soon![/yellow]")
    console.print("[dim]For now, use the MCP server mode: pyclarity server[/dim]")


# Add the examples command to the CLI
app.command(name="examples")(examples_command)
