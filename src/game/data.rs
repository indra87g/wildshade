use std::collections::HashMap;
use crate::game::enemy::Enemy;
use fake::Fake;
use fake::faker::name::en::FirstName;

pub fn get_fake_name() -> String {
    FirstName().fake()
}

pub fn items_for_sale() -> HashMap<String, i32> {
    let mut m = HashMap::new();
    m.insert("Stone Sword".to_string(), 30);
    m.insert("Stone Axe".to_string(), 20);
    m.insert("Stone Pickaxe".to_string(), 1);
    m.insert("Shield".to_string(), 25);
    m.insert("Health Potion".to_string(), 25);
    m.insert("Cooked Chicken".to_string(), 10);
    m.insert("Bread".to_string(), 5);
    m
}

pub fn items_durability() -> HashMap<String, i32> {
    let mut m = HashMap::new();
    m.insert("Stone Sword".to_string(), 50);
    m.insert("Stone Axe".to_string(), 50);
    m.insert("Stone Pickaxe".to_string(), 50);
    m
}

pub fn quests() -> HashMap<String, Vec<i32>> {
    let mut m = HashMap::new();
    m.insert("combat".to_string(), vec![10, 20, 50, 100]);
    m.insert("mining".to_string(), vec![10, 20, 50, 100]);
    m
}

pub fn initial_stats() -> HashMap<String, i32> {
    let mut m = HashMap::new();
    m.insert("enemy_defeated".to_string(), 0);
    m.insert("foods_eat".to_string(), 0);
    m.insert("stone_collected".to_string(), 0);
    m.insert("wood_collected".to_string(), 0);
    m
}

pub fn enemies() -> Vec<Enemy> {
    vec![
        Enemy::new("Wolf", 30, "A wild wolf is growling at you!", 10, 20, 15, 1),
        Enemy::new("Gnoll", 25, "A quick brown gnoll is angry to see you!", 15, 20, 10, 1),
    ]
}
