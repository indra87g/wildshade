from rich.table import Table

from game.utils.ui import c


class Inventory:
    def __init__(self) -> None:
        self.items = {}

    def add_item(self, item: str, quantity=1) -> None:
        """Add item to inventory."""
        if item in self.items:
            self.items[item] += quantity
        else:
            self.items[item] = quantity
        c.print(f"[bold green]Added {quantity}x {item} to inventory.[/bold green]")

    def remove_item(self, item: str, quantity=1) -> None:
        """Remove item from inventory."""
        if item in self.items:
            if self.items[item] > quantity:
                self.items[item] -= quantity
                c.print(f"[bold yellow]Removed {quantity}x {item} from invrntory.")
            else:
                del self.items[item]
                c.print(f"[bold red]{item} removed from inventory.")
        else:
            c.print(f"[bold red]{item} not found in inventory.")

    def show_inventory(self) -> None:
        """Show inventory in table."""
        if not self.items:
            c.print("[bold red]Your inventory is empty.[/bold red]")
            return

        table = Table(title="[bold cyan]Inventory")
        table.add_column("Item", style="bold yellow")
        table.add_column("Quantity", justify="right", style="bold green")

        for item, quantity in self.items.items():
            table.add_row(item, str(quantity))

        c.print(table)

    def to_dict(self) -> None:
        """Save inventory into dictionary."""
        return self.items

    def from_dict(self, data) -> None:
        """Load inventory from dictionary."""
        self.items = data
