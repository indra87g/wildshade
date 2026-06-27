use serde::{Deserialize, Serialize};
use crate::game::inventory::Inventory;
use crate::game::quest::Quest;
use crate::game::enemy::Enemy;
use crate::game::data::{enemies, items_durability};
use crate::utils::ui::print_color;
use crate::utils::logger::{log_info, log_warning};
use std::fs::File;
use std::io::{Read, Write};
use inquire::Select;

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Player {
    pub name: String,
    pub coins: f64,
    pub health: i32,
    pub hunger: i32,
    pub thirst: i32,
    pub energy: i32,
    pub level: i32,
    pub xp: i32,
    pub inventory: Inventory,
    pub quest: Quest,
    #[serde(skip)]
    pub savegame_notfound: bool,
    #[serde(skip)]
    pub items_durability: std::collections::HashMap<String, i32>,
}

impl Player {
    pub fn new(name: String) -> Self {
        Self {
            name,
            coins: 10.0,
            health: 100,
            hunger: 0,
            thirst: 0,
            energy: 100,
            level: 1,
            xp: 0,
            inventory: Inventory::new(),
            quest: Quest::new(),
            savegame_notfound: false,
            items_durability: items_durability(),
        }
    }

    pub fn show_status(&self) {
        println!("--- Status ---");
        print_color(&format!("Name: {}", self.name), "yellow");
        print_color(&format!("Level {} | XP: {}", self.level, self.xp), "cyan");
        print_color(&format!("Health: {}/100", self.health), "red");
        print_color(&format!("Hunger: {}/100 | Thirst: {}/100", self.hunger, self.thirst), "yellow");
        print_color(&format!("Energy {}/100", self.energy), "magenta");
        print_color(&format!("Coins: {}", self.coins), "green");
        println!("--------------");
    }

    pub fn explore(&mut self) {
        print_color("You are exploring wilderness...", "green");
        let encounter_type = ["food", "enemy", "loot", "nothing"];
        let idx = rand::random_range(0..encounter_type.len());
        let encounter = encounter_type[idx];

        match encounter {
            "food" => {
                let foods = ["Apple", "Chicken", "Meat"];
                let food = foods[rand::random_range(0..foods.len())];
                self.inventory.add_item(food, 1);
                self.gain_xp(10);
            }
            "enemy" => {
                print_color("You encountered an enemy!", "red");
                self.fight();
            }
            "loot" => {
                let loots = ["Gold Ring", "Silver Gauntlet", "Old Map"];
                let loot = loots[rand::random_range(0..loots.len())];
                self.inventory.add_item(loot, 1);
                print_color(&format!("You found a {}!", loot), "green");
            }
            _ => {
                if *self.quest.stats.get("enemy_defeated").unwrap_or(&0) == 10 {
                    print_color("You defeated 10 enemies! Claim gift in Quest", "magenta");
                } else {
                    print_color("You found nothing", "cyan");
                }
            }
        }
    }

    pub fn eat(&mut self, food: &str) {
        if self.inventory.items.contains_key(food) {
            self.inventory.remove_item(food, 1);
            self.health = (self.health + 10).min(100);
            self.hunger = (self.hunger - 15).max(0);
            self.energy = (self.energy + 10).min(100);
            self.gain_xp(5);
            print_color(&format!("You ate {} and gained energy!", food), "green");
        } else {
            print_color(&format!("You don't have {} to eat!", food), "red");
        }
    }

    pub fn drink(&mut self) {
        if self.inventory.items.contains_key("Water Bottle") {
            self.inventory.remove_item("Water Bottle", 1);
            self.thirst = (self.thirst - 20).max(0);
            self.energy = (self.energy + 5).min(100);
            self.gain_xp(5);
            print_color("You drank water and feel refreshed!", "blue");
        } else {
            print_color("You don't have any water!", "red");
        }
    }

    pub fn fight(&mut self) {
        let enemy_list = enemies();
        let base_enemy = &enemy_list[rand::random_range(0..enemy_list.len())];
        let mut enemy = Enemy::new(
            &base_enemy.name,
            base_enemy.health,
            &base_enemy.description,
            base_enemy.damage,
            base_enemy.xp,
            base_enemy.coins,
            base_enemy.level,
        );

        print_color(&format!("\nA {} appears! {}", enemy.name, enemy.description), "red");

        while enemy.is_alive() && self.health > 0 {
            let options = vec!["Attack", "Defend", "Run"];
            let action = Select::new("Choose your action:", options).prompt().unwrap();

            match action {
                "Attack" => {
                    let damage = rand::random_range(10..=20);
                    enemy.take_damage(damage);
                    print_color(&format!("You hit {} for {} damage!", enemy.name, damage), "green");
                    self.show_health_bar(&enemy.name, enemy.health, 100);
                }
                "Defend" => {
                    print_color("You brace yourself for the enemy's attack!", "blue");
                    let damage_taken = (enemy.attack() - rand::random_range(3..=10)).max(0);
                    self.health -= damage_taken;
                    print_color(&format!("You take {} damage", damage_taken), "yellow");
                }
                "Run" => {
                    if rand::random_bool(0.5) {
                        print_color("You successfully escaped!", "green");
                        return;
                    } else {
                        print_color(&format!("{} is blocking your way!", enemy.name), "red");
                    }
                }
                _ => unreachable!(),
            }

            if enemy.is_alive() {
                let damage = enemy.attack();
                self.health -= damage;
                print_color(&format!("{} attacks you for {} damage!", enemy.name, damage), "red");
                self.show_health_bar(&self.name, self.health, 100);
            }
        }

        if self.health <= 0 {
            print_color("You has been defeated!", "red");
        } else {
            print_color(&format!("You defeated {}!", enemy.name), "green");
            self.gain_xp(enemy.xp);
            self.coins += enemy.coins as f64;
            self.hunger = (self.hunger + rand::random_range(5..=10)).min(100);
            self.thirst = (self.thirst + rand::random_range(5..=10)).min(100);
            let defeated = self.quest.stats.entry("enemy_defeated".to_string()).or_insert(0);
            *defeated += 1;
        }
    }

    pub fn mining(&mut self, hours: i32) {
        if self.inventory.items.contains_key("Stone Pickaxe") {
            print_color("You are mining...", "green");
            let stone = rand::random_range(10..=50);
            println!("--- Mining Result ---");
            print_color(&format!("Time: {} Hours", hours), "blue");
            print_color(&format!("Stone Collected: {}", stone), "magenta");
            print_color(&format!("Estimated Profit: {}c", stone as f64 / 2.0), "purple");
            print_color("XP Gained: 10", "purple");
            println!("----------------------");

            self.item_durability(10, "Stone Pickaxe");
            self.coins += stone as f64 / 2.0;
            self.gain_xp(10);
            let collected = self.quest.stats.entry("stone_collected".to_string()).or_insert(0);
            *collected += stone;
        } else {
            print_color("You don't have a Pickaxe!", "red");
        }
    }

    pub fn rest(&mut self, hours: i32) {
        print_color("You are resting...", "cyan");
        self.energy = (self.energy + (hours * 10)).min(100);
        self.health = (self.health + (hours * 10)).min(100);
        self.hunger = (self.hunger + hours).min(100);
        self.thirst = (self.thirst + (hours + 10)).min(100);
    }

    pub fn check_status(&self) -> bool {
        if self.health <= 0 || self.energy <= 0 || self.hunger >= 100 || self.thirst >= 100 {
            print_color("GAME OVER!", "red");
            false
        } else {
            print_color("You are still surviving!", "green");
            true
        }
    }

    pub fn item_durability(&mut self, amount: i32, item: &str) {
        if let Some(durability) = self.items_durability.get_mut(item) {
            *durability -= amount;
            if *durability < 1 {
                print_color(&format!("Oh no, your {} is broken!", item), "red");
                self.inventory.remove_item(item, 1);
            }
        }
    }

    pub fn gain_xp(&mut self, amount: i32) {
        self.xp += amount;
        if self.xp >= self.level * 100 {
            self.xp -= self.level * 100;
            self.level += 1;
            self.health = 100;
            print_color(&format!("You leveled up to level {}!", self.level), "blue");
        }
    }

    pub fn show_health_bar(&self, name: &str, current_hp: i32, max_hp: i32) {
        if current_hp > 0 {
            let bar_length = ((current_hp as f64 / max_hp as f64) * 20.0) as usize;
            let bar = format!("{}{}", "█".repeat(bar_length), "-".repeat(20 - bar_length));
            println!("{}'s HP: {}/{} [{}]", name, current_hp, max_hp, bar);
        }
    }

    pub fn save_game(&self, filename: &str) {
        let data = serde_json::to_string(self).unwrap();
        let mut file = File::create(filename).unwrap();
        file.write_all(data.as_bytes()).unwrap();
        print_color(&format!("Game saved to {}", filename), "green");
        log_info(&format!("Game saved to {}", filename));
    }

    pub fn load_game(&mut self, filename: &str) {
        match File::open(filename) {
            Ok(mut file) => {
                let mut data = String::new();
                file.read_to_string(&mut data).unwrap();
                let loaded_player: Player = serde_json::from_str(&data).unwrap();
                *self = loaded_player;
                self.items_durability = items_durability();
                self.savegame_notfound = false;
                print_color(&format!("Game loaded from {}", filename), "green");
                log_info(&format!("Game loaded from {}", filename));
            }
            Err(_) => {
                self.savegame_notfound = true;
                print_color("Savegame not found! Starting new game.", "red");
                log_warning("No savegame found. Starting new game.");
            }
        }
    }
}
