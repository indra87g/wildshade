from faker.proxy import Faker

from game.enemy import Enemy
import faker

fake: Faker = faker.Faker()
fake_name: str = fake.first_name()

items_for_sale = {
    "Stone Sword": 30,
    "Stone Axe": 20,
    "Stone Pickaxe": 1,
    "Shield": 25,
    "Health Potion": 25,
    "Cooked Chicken": 10,
    "Bread": 5,
}

items_durability = {"Stone Sword": 50, "Stone Axe": 50, "Stone Pickaxe": 50}

quests = {"combat": [10, 20, 50, 100], "mining": [10, 20, 50, 100]}

stats = {
    "enemy_defeated": 0,
    "foods_eat": 0,
    "stone_collected": 0,
    "wood_collected": 0,
}

wolf: Enemy = Enemy("Wolf", 30, "A wild wolf is growling at you!", 10, 20, 15)
gnoll: Enemy = Enemy(
    "Gnoll", 25, "A quick brown gnoll is angry to see you!", 15, 20, 10
)

enemies = [wolf, gnoll]
