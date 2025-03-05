import random


class Enemy:
    def __init__(self, name: str, health: int, description: str, damage: int, xp: int, coins: int, level=1) -> None:
        self.name = name
        self.level = level
        self.health = health + level * 5
        self.description = description
        self.damage = damage + level * 2
        self.xp = xp
        self.coins = coins

    def attack(self) -> int:
        return random.randint(self.damage - 5, self.damage + 5)

    def take_damage(self, amount: int) -> None:
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_alive(self) -> bool:
        return self.health > 0
