from rich.panel import Panel

from game.utils.ui import c
from game.data import stats


class Quest:
    def __init__(self) -> None:
        self.stats = stats

    def show_quest(self) -> None:
        quest = f"""
        I. Combat
        {self.defeat_enemy()}

        II. Mining
        {self.mine_stone()}

        III. Gourmet
        Eat 10 Foods
        """
        c.print(Panel(quest, title="Active Quest", expand=False))

    def defeat_enemy(self) -> str:
        if self.stats["enemy_defeated"] in range(0, 9):
            return "[italic green]Defeat 10 Enemy[/italic green]"
        elif self.stats["enemy_defeated"] in range(10, 19):
            return "[italic green]Defeat 20 Enemy[/italic green]"
        elif self.stats["enemy_defeated"] in range(20, 29):
            return "[italic green]Defeat 50 Enemy[/italic green]"
        elif self.stats["enemy_defeated"] in range(30, 99):
            return "[bold green]Defeat 100 Enemy[/bold green]"
        elif self.stats["enemy_defeated"] in range(100, 999999999):
            return f"""
        [bold magenta]Quest Combat Complete![/bold magenta]
        [italic yellow]Enemy Defeated: {self.stats["enemy_defeated"]}[/italic yellow]
        """

    def mine_stone(self) -> str:
        if self.stats["stone_collected"] in range(0, 19):
            return "[italic blue]Mine 20 Stone[/italic blue]"
        elif self.stats["stone_collected"] in range(20, 39):
            return "[italic blue]Mine 40 Stone[/italic blue]"
        elif self.stats["stone_collected"] in range(40, 59):
            return "[italic blue]Mine 60 Stone[/italic blue]"
        elif self.stats["stone_collected"] in range(60, 79):
            return "[italic blue]Mine 80 Stone[/italic blue]"
        elif self.stats["stone_collected"] in range(80, 99):
            return "[italic blue]Mine 100 Stone[/italic blue]"
        elif self.stats["stone_collected"] in range(100, 999999999):
            return f"""
        [bold magenta]Quest Mining Complete![/bold magenta]
        [italic yellow]Stone Collected: {self.stats["stone_collected"]}[/italic yellow]
        """

    def to_dict(self) -> None:
        return self.stats

    def from_dict(self, data) -> None:
        self.stats = data
