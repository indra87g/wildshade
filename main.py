from rich.prompt import Prompt
from click.termui import pause, clear
from platform import python_version

from game.player import Player
from game.utils.ui import c
from game.utils.logger import log_info, log_warning, truncate_log
from game.data import fake_name


def next_turn(player=None, check_status=True, player_class=True) -> None:
    if player_class:
        if check_status:
            player.check_status()
            pause()
            main(player)
        else:
            pause()
            main(player)
    else:
        pause()
        clear()


def welcome() -> None:
    c.print("[bold cyan]Welcome to Wildshade![/bold cyan]\n")
    next_turn(player_class=False, check_status=False)


def explore(player) -> None:
    clear()
    c.print("\n[bold blue]What would like to do?[/bold blue]")
    explore_action = Prompt.ask(
        "[bold yellow](E)xplore / (Q)uest[/bold yellow]"
    ).lower()
    if explore_action == "e":
        player.explore()
    elif explore_action == "q":
        player.quest.show_quest()
    next_turn(player)


def consume(player) -> None:
    clear()
    c.print("\n[bold blue]What would like to do?[/bold blue]")
    consume_action = Prompt.ask("[bold yellow](E)at / (D)rink[/bold yellow]").lower()
    if consume_action == "e":
        food = Prompt.ask("[bold blue]Enter food name to eat:[/bold blue]")
        player.eat(food)
    elif consume_action == "d":
        player.drink()
    next_turn(player)


def work(player) -> None:
    clear()
    c.print("\n[bold blue]What would like to do?[/bold blue]")
    work_action = Prompt.ask(
        "[bold yellow](M)ining / (W)oodcutting[/bold yellow]"
    ).lower()
    if work_action == "m":
        hours = int(
            Prompt.ask("[bold blue]How many hours do you want to mine?[/bold blue]")
        )
        player.mining(hours)
    elif work_action == "w":
        player.woodcutting()
    next_turn(player)


def shop(player) -> None:
    clear()
    player.shop.show_shop()
    c.print("\n[bold blue]What would like to do?[/bold blue]")
    shop_action = Prompt.ask("[bold yellow](B)uy / (S)ell[/bold yellow]").lower()
    if shop_action == "b":
        item = Prompt.ask("[bold blue]Enter item name to buy:[/bold blue]")
        player.shop.buy(player, item)
    elif shop_action == "s":
        item = Prompt.ask("[bold blue]Enter item name to sell:[/bold blue]")
        player.shop.sell(player, item)
    next_turn(player, check_status=False)


def main(player) -> None:
    clear()
    player.show_status()
    c.print("\n[bold blue]What would like to do?[/bold blue]")
    action = Prompt.ask(
        "[bold yellow](E)xplore / (C)onsume / (W)ork / (R)est / (I)nventory / (Sh)op / (Q)uit[/bold yellow]"
    ).lower()

    if action == "e":
        explore(player)
    elif action == "c":
        consume(player)
    elif action == "w":
        work(player)
    elif action == "r":
        hours = int(
            Prompt.ask("[bold blue]How many hours do you want to sleep?[/bold blue]")
        )
        player.rest(hours)
        next_turn(player)
    elif action == "i":
        player.inventory.show_inventory()
        next_turn(player, check_status=False)
    elif action == "sh":
        shop(player)
    elif action == "q":
        player.save_game()
        c.print("[bold red]Thanks for playing! Come back soon![/bold red]")
        log_info("Program closed with (Q)uit.")
        exit()
    elif action == "save":
        player.save_game()
        next_turn(player, check_status=False)
    elif action == "load":
        player.load_game()
        next_turn(player, check_status=False)
    else:
        c.print("[bold red]Invalid action! Try again.[/bold red]")
        next_turn(player, check_status=False)


if __name__ == "__main__":
    truncate_log()
    log_info(f"Program started on Python {python_version()}")
    welcome()
    try:
        name: str = Prompt.ask("\n[bold yellow]Enter your name[/bold yellow]")

        if not name:
            log_warning("'name' is not provided, using fake name instead.")
            player = Player(fake_name)
        else:
            player = Player(name)
        main(player)
    except KeyboardInterrupt:
        c.print("[bold red]Program closed.[/bold red]")
        log_info("Program closed with CTRL+C.")
