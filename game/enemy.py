import random


class Enemy:
    def __init__(
        self, name: str, health: int, description: str, damage: int, xp: int, coins: int
    ) -> None:
        self.name = name
        self.health = health
        self.description = description
        self.damage = damage
        self.xp = xp
        self.coins = coins

    def attack(self) -> int:
        return random.randint(self.damage - 5, self.damage + 5)

    def is_alive(self) -> bool:
        return self.health > 0
