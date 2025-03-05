from rich.panel import Panel

from game.utils.ui import c
from game.data import quests, stats


class Quest:
    def __init__(self) -> None:
        self.quests = quests
        self.stats = stats

    def show_quest(self) -> None:
        quest = f"""
        I. Combat
        {self.quest_progress("enemy_defeated", "Defeat", self.quests["combat"], "Enemy", "green")}

        II. Mining
        {self.quest_progress("stone_collected", "Mine", self.quests["mining"], "Stone", "blue")}
        """
        c.print(Panel(quest, title="Active Quest", expand=False))

    def quest_progress(
        self, key: str, action: str, milestones: list, item: str, color: str
    ) -> str:
        value = self.stats.get(key, 0)

        for milestone in milestones:
            if value < milestone:
                return f"[italic {color}]{action} {milestone} {item}[/italic {color}]"
            elif value > 100:
                return f"[italic magenta]Complete | {action} {self.stats[key]} {item}[/italic magenta]"

        return f"""
        [bold magenta]Quest {action} Complete![/bold magenta]
        [italic yellow]{action} Count: {value}[/italic yellow]
        """

    def to_dict(self) -> None:
        return self.stats

    def from_dict(self, data) -> None:
        self.stats = data
