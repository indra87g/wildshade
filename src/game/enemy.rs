use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Enemy {
    pub name: String,
    pub level: i32,
    pub health: i32,
    pub description: String,
    pub damage: i32,
    pub xp: i32,
    pub coins: i32,
}

impl Enemy {
    pub fn new(name: &str, health: i32, description: &str, damage: i32, xp: i32, coins: i32, level: i32) -> Self {
        Self {
            name: name.to_string(),
            level,
            health: health + level * 5,
            description: description.to_string(),
            damage: damage + level * 2,
            xp,
            coins,
        }
    }

    pub fn attack(&self) -> i32 {
        rand::random_range((self.damage - 5).max(0)..=(self.damage + 5))
    }

    pub fn take_damage(&mut self, amount: i32) {
        self.health = (self.health - amount).max(0);
    }

    pub fn is_alive(&self) -> bool {
        self.health > 0
    }
}
