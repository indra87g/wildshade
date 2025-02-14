from rich.table import Table

from game.utils.ui import c
from game.utils.logger import log_info, log_warning
from game.data import items_for_sale


class Shop:
    def __init__(self) -> None:
        """Save item list for shop."""
        self.items_for_sale = items_for_sale
        self.sell_prices = {
            item: price // 2 for item, price in self.items_for_sale.items()
        }
        log_info("Class 'Shop' loaded.")

    def show_shop(self) -> None:
        """Show item list for shop in table."""
        table = Table(title="[bold cyan]Shop")
        table.add_column("Item", style="bold yellow")
        table.add_column("Price", justify="right", style="bold green")

        for item, price in self.items_for_sale.items():
            table.add_row(item, f"{price}c")

        c.print(table)

    def buy(self, player, item: str) -> None:
        """Buy item from shop."""
        if item in self.items_for_sale:
            price = self.items_for_sale[item]
            if player.coins >= price:
                c.print(f"[bold green]You bought {item} for {price}")
                player.inventory.add_item(item)
            else:
                c.print(f"[bold red]Not enough coins to buy {item}")
        else:
            c.print(f"[bold red]{item} is not found in the shop")
            log_warning(f"'{item}' is not found in 'items_for_sale'.")

    def sell(self, player, item: str) -> None:
        """Sell item to shop."""
        if item in player.inventory.items:
            price = self.sell_prices.get(item, 0)
            player.inventory.remove_item(item)
            player.coins += price
            c.print(f"[bold green]You sold {item} for {price}c")
        else:
            c.print(f"[bold red]You don't have {item} to sell")
