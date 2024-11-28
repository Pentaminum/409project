import os
import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.panel import Panel
from rich.live import Live
from rich.spinner import Spinner
from .document_loader import DocumentLoader
from .vector_store import VectorStore
from .chat import ChatInterface
from .config import DOCUMENT_TYPES

console = Console()

class CLI:
    def __init__(self):
        self.console = Console()
        self.history = []
        self.vector_store = None
        self.chat_interface = None
        
    def initialize_system(self):
        try:
            with console.status("[bold green]Initializing system...") as status:
                # Load documents
                status.update("[bold green]Loading documents...")
                loader = DocumentLoader()
                documents = loader.load_directory()  # Load all directories
                
                if not documents:
                    raise Exception("No documents were loaded successfully")
                
                # Create vector store
                status.update("[bold green]Creating vector store...")
                self.vector_store = VectorStore()
                self.vector_store.create_vector_store(documents)
                
                # Initialize chat interface
                status.update("[bold green]Initializing chat interface...")
                self.chat_interface = ChatInterface(self.vector_store)
                
            console.print("\n[bold green]✓ System initialized successfully!")
            
        except Exception as e:
            console.print(f"\n[bold red]Error initializing system: {str(e)}")
            sys.exit(1)

    def display_welcome(self):
        welcome_text = """
# 🤖 LangChain Chat Interface

- Type your questions and press Enter to get responses
- Type 'exit' or 'quit' to end the session
- Type 'clear' to clear the chat history
- Type 'help' to see these instructions again
"""
        console.print(Markdown(welcome_text))

    def display_response(self, response):
        # Display the main response
        console.print("\n[bold blue]Assistant:[/bold blue]")
        console.print(Panel(Markdown(response["answer"]), border_style="blue"))
        
        # Display sources if available
        if response.get("source_documents"):
            console.print("\n[bold cyan]Sources:[/bold cyan]")
            for doc in response["source_documents"]:
                source = doc.metadata['source']
                directory = doc.metadata['directory']
                # Get document type description if available
                doc_type = next((k for k, v in DOCUMENT_TYPES.items() 
                               if k in directory), "other")
                desc = DOCUMENT_TYPES.get(doc_type, {}).get("description", "")
                console.print(f"- [cyan]{source}[/cyan]")
                if desc:
                    console.print(f"  [dim]{desc}[/dim]")

    def run(self):
        self.display_welcome()
        self.initialize_system()

        while True:
            try:
                # Get user input
                query = Prompt.ask("\n[bold green]You")
                
                # Handle commands
                if query.lower() in ['exit', 'quit']:
                    console.print("[yellow]Goodbye! 👋[/yellow]")
                    break
                elif query.lower() == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.display_welcome()
                    continue
                elif query.lower() == 'help':
                    self.display_welcome()
                    continue
                
                # Show thinking spinner
                with console.status("[bold yellow]Thinking..."):
                    response = self.chat_interface.chat(query)
                
                # Display response
                self.display_response(response)

            except KeyboardInterrupt:
                console.print("\n[yellow]Exiting...[/yellow]")
                break
            except Exception as e:
                console.print(f"\n[red]Error: {str(e)}[/red]")

if __name__ == "__main__":
    cli = CLI()
    cli.run()