import asyncio
import os
import sys

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.live import Live
import time
from app.cli.llm_agent import run_agent

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


console = Console()

async def main_cli():
    console.print(Panel("[bold green]Bem-vindo ao Assistente de Automóveis Virtual![/bold green]",
                        subtitle="Impulsionado por IA."))
    console.print("Deseja consultar os veículos disponíveis?")
    console.print("Para sair, digite 'sair'.\n")

    while True:
        user_input = console.input("[bold blue]Você: [/bold blue]")
        if user_input.lower() == "sair":
            console.print(Panel("[bold yellow]Até logo![/bold yellow]", border_style="yellow"))
            break

        with Live(Text("O agente está pensando...", style="italic blue"), console=console, screen=False, refresh_per_second=4) as live:
            agent_response = await run_agent(user_input)
            live.stop()

        console.print(Panel(Text(agent_response, style="green"), title="[bold green]Agente Automóveis[/bold green]"))
        console.print("")

if __name__ == "__main__":
    asyncio.run(main_cli())