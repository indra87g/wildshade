import random
import json
from rich.prompt import Prompt
from rich.panel import Panel

from game.inventory import Inventory
from game.shop import Shop
from game.enemy import Enemy
from game.quest import Quest
from game.data import enemies, items_durability
from game.utils.logger import log_info, log_warning

from game.utils.ui import c


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.coins = 10
        self.health = 100
        self.hunger = 0
        self.thirst = 0
        self.energy = 100
        self.level = 1
        self.xp = 0
        self.inventory = Inventory()
        self.shop = Shop()
        self.quest = Quest()
        self.savegame_notfound = None

    def show_status(self) -> None:
        """Show player status using Rich Panel."""
        status = f"""
        [bold yellow]Name:[/bold yellow] {self.name}
        [bold cyan]Level[/bold cyan] {self.level} | [bold green]XP:[/bold green]{self.xp}
        [bold red]Health:[/bold red] {self.health}/100
        [bold yellow]Hunger:[/bold yellow] {self.hunger}/100 | [bold blue]Thirst:[/bold blue] {self.thirst}/100
        [bold magenta]Energy[/bold magenta] {self.energy}/100
        [bold green]Coins:[/bold green] {self.coins}
        """
        c.print(Panel(status, title="[bold blue]Status[/bold blue]", expand=False))

    def explore(self) -> None:
        """Explore the world and get item or encounter something."""
        c.print("[bold green]You are exploring wilderness...[/bold green]")
        encounter = random.choice(["food", "enemy", "loot", "nothing"])

        if encounter == "food":
            food = random.choice(["Apple", "Chicken", "Meat"])
            self.inventory.add_item(food)
            self.gain_xp(10)
        elif encounter == "enemy":
            c.print("[bold red]You encountered an enemy![/bold red]")
            self.fight()
        elif encounter == "loot":
            loot = random.choice(["Gold Ring", "Silver Gauntlet", "Old Map"])
            self.inventory.add_item(loot)
            c.print(f"[bold green]You found a {loot}![/bold green]")
        elif self.quest.stats["enemy_defeated"] == 10:
            c.print(
                "[bold magenta]You defeated 10 enemies! Claim gift in Quest[/bold magenta]"
            )
        else:
            c.print("[bold cyan]You found nothing[/bold cyan]")

    def eat(self, food: str) -> None:
        """Eat food in inventory."""
        if food in self.inventory.items:
            self.inventory.remove_item(food)
            self.health = min(self.health + 10, 100)
            self.hunger = max(self.hunger - 15, 0)
            self.energy = min(self.energy + 10, 100)
            self.gain_xp(5)
            c.print(f"[bold green]You ate {food} and gained energy![/bold green]")
        else:
            c.print(f"[bold red]You don't have {food} to eat![/bold red]")

    def drink(self) -> None:
        """Drink water in inventory."""
        if "Water Bottle" in self.inventory.items:
            self.inventory.remove_item("Water Bottle")
            self.thirst = max(self.thirst - 20, 0)
            self.energy = min(self.energy + 5, 100)
            self.gain_xp(5)
            c.print("[bold blue]You drank water and feel refreshed![/bold blue]")
        else:
            c.print("[bold red]You don't have any water![/bold red]")

    def fight(self) -> None:
        enemy = random.choice(enemies)
        enemy = Enemy(
            enemy.name,
            enemy.health,
            enemy.description,
            enemy.damage,
            enemy.xp,
            enemy.coins,
        )

        c.print(f"\n[bold red]A {enemy.name} appears![/bold red] {enemy.description}")

        while enemy.is_alive() and self.health > 0:
            c.print("\n[bold blue]Choose your action:[/bold blue]")
            action = Prompt.ask("(A)ttack / (D)efend / (R)un").lower()

            if action == "a":
                damage = random.randint(10, 20)
                enemy.health -= damage
                c.print(
                    f"[bold green]You hit {enemy.name} for {damage} damage![/bold green]"
                )
                self.show_health_bar(enemy.name, enemy.health)
            elif action == "d":
                c.print(
                    "[bold blue]You brace yourself for the enemy's attack![/bold blue]"
                )
                damage_taken = max(enemy.attack() - random.randint(3, 10), 0)
                self.health -= damage_taken
                c.print(f"[bold yellow]You take {damage_taken} damage[/bold yellow]")
            elif action == "r":
                is_escaped = random.choice([True, False])
                if is_escaped:
                    c.print("[bold green]You successfully escaped![/bold green]")
                    return
                else:
                    c.print(f"[bold red]{enemy.name} is blocking your way![/bold red]")
            else:
                c.print("[bold red]Invalid action![/bold red]")

            if enemy.is_alive():
                damage = enemy.attack()
                self.health -= damage
                c.print(
                    f"[bold red]{enemy.name} attacks you for {damage} damage![/bold red]"
                )
                self.show_health_bar(self.name, self.health)

        if self.health <= 0:
            c.print("[bold red]You has been defeated![/bold red]")
        else:
            c.print(f"[bold green]You defeated {enemy.name}![/bold green]")
            self.gain_xp(enemy.xp)
            self.coins += enemy.coins
            self.hunger = min(self.hunger + random.randint(5, 10), 100)
            self.thirst = min(self.thirst + random.randint(5, 10), 100)
            self.quest.stats["enemy_defeated"] += 1

    def mining(self, hours: int) -> None:
        if "Stone Pickaxe" in self.inventory.items:
            c.print("[bold green]You are mining...[/bold green]")
            stone = random.randint(10, 50)
            result = f"""
            [bold blue]Time:[/bold blue] {hours} Hours
            [bold magenta]Stone Collected:[/bold magenta] {stone}


            [bold purple]Estimated Profit:[/bold purple] {stone / 2}c
            [bold purple]XP Gained:[/bold purple] 10
            """
            self.item_durability(10, "Stone Pickaxe")
            c.print(
                Panel(
                    result, title="[bold green]Mining Result[/bold green]", expand=False
                )
            )
            self.coins += stone / 2
            self.gain_xp(10)
            self.quest.stats["stone_collected"] += stone
        else:
            c.print("[bold red]You don't have a Pickaxe![/bold red]")

    def rest(self, hours: int) -> None:
        """Sleep for player-defined time."""
        c.print("[bold cyan]You are resting...[/bold cyan]")
        self.energy = min(self.energy + (hours * 10), 100)
        self.health = min(self.health + (hours * 10), 100)
        self.hunger = min(self.hunger + hours, 100)
        self.thirst = min(self.hunger + (hours + 10), 100)

    def check_status(self) -> None:
        """Check if player is alive or not."""
        if (
            self.health <= 0
            or self.energy <= 0
            or self.hunger >= 100
            or self.thirst >= 100
        ):
            c.print("[bold red]GAME OVER![/bold red]")
            exit()
        else:
            c.print("[bold green]You are still surviving![/bold green]")

    def item_durability(self, amount: int, item: str) -> None:
        items_durability[item] -= amount
        if items_durability[item] < 1:
            c.print(f"[bold red]Oh no, your {item} is broken![/bold red]")
            self.inventory.remove_item(item)

    def gain_xp(self, amount: int) -> None:
        """Give XP to player."""
        self.xp += amount
        if self.xp >= self.level * 100:
            self.xp -= self.level * 100
            self.level += 1
            self.health = 100
            c.print(f"[bold blue]You leveled up to level {self.level}!")

    def show_health_bar(self, name: str, current_hp: int, max_hp=100) -> None:
        if current_hp > 0:
            bar_length: int = int((current_hp / max_hp) * 20)
            health_bar = "█" * bar_length + "-" * (20 - bar_length)
            c.print(f"[bold]{name}'s HP: {current_hp}/{max_hp}[/bold] [{health_bar}]\n")
        else:
            pass

    def save_game(self, filename="savegame.json") -> None:
        """Save game."""
        data = {
            "name": self.name,
            "coins": self.coins,
            "health": self.health,
            "hunger": self.hunger,
            "thirst": self.thirst,
            "energy": self.energy,
            "level": self.level,
            "xp": self.xp,
            "inventory": self.inventory.to_dict(),
            "quest_stats": self.quest.to_dict(),
        }
        with open(filename, "w") as f:
            json.dump(data, f)
        c.print(f"[bold green]Game saved to {filename}[/bold green]")
        log_info(f"Game saved to {filename}")

    def load_game(self, filename="savegame.json") -> None:
        """Save game"""
        try:
            with open(filename, "r") as f:
                data: dict = json.load(f)

            self.name = data["name"]
            self.coins = data["coins"]
            self.health = data["health"]
            self.hunger = data["hunger"]
            self.thirst = data["thirst"]
            self.energy = data["energy"]
            self.level = data["level"]
            self.xp = data["xp"]
            self.inventory.from_dict(data["inventory"])
            self.quest.from_dict(data["quest_stats"])
            self.savegame_notfound = False
            c.print(f"[bold green]Game loaded from {filename}[/bold green]")
            log_info(f"Game loaded from {filename}")
        except FileNotFoundError:
            self.savegame_notfound = True
            c.print("[bold red]Savegame not found! Starting new game.[/bold red]")
            log_warning("No savegame found. Starting new game.")
