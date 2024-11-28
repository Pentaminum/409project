from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.columns import Columns
from rich import box
from src.cli import CLI
from src.ui.server import app
import webbrowser
import threading
import time

console = Console()

def open_browser():
    time.sleep(1.5)  # Wait for server to start
    webbrowser.open('http://localhost:5000')

def display_menu():
    console.clear()
    console.print(Panel(
        "[bold cyan]CMPT 409/981 AI Assistant[/bold cyan]\n\n" +
        "Select interface mode using arrow keys:",
        box=box.ROUNDED
    ))
    
    options = [
        Panel("[1] Terminal Interface", style="green", box=box.ROUNDED),
        Panel("[2] Web Interface", style="white", box=box.ROUNDED)
    ]
    
    console.print(Columns(options))

def get_user_choice():
    choices = {
        "1": ("Terminal Interface", False),
        "2": ("Web Interface", True)
    }
    
    choice = Prompt.ask(
        "\n[yellow]Choose interface[/yellow]",
        choices=["1", "2"],
        default="1"
    )
    
    return choices[choice]

def main():
    display_menu()
    interface_name, use_web = get_user_choice()
    
    console.print(f"\n[bold green]Starting {interface_name}...[/bold green]")
    
    if use_web:
        console.print("\n[bold green]Starting web server...[/bold green]")
        # Start browser in a separate thread
        threading.Thread(target=open_browser, daemon=True).start()
        # Start Flask server
        app.run(debug=False)  # Set debug=False to avoid reloader
    else:
        cli = CLI()
        cli.run()

if __name__ == "__main__":
    main()