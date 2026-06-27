use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use crate::game::data::{quests, initial_stats};

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Quest {
    pub stats: HashMap<String, i32>,
}

impl Quest {
    pub fn new() -> Self {
        Self {
            stats: initial_stats(),
        }
    }

    pub fn show_quest(&self) {
        println!("Active Quests:");
        let q = quests();

        println!("I. Combat");
        println!("{}", self.quest_progress("enemy_defeated", "Defeat", &q["combat"], "Enemy", "green"));

        println!("II. Mining");
        println!("{}", self.quest_progress("stone_collected", "Mine", &q["mining"], "Stone", "blue"));
    }

    fn quest_progress(&self, key: &str, action: &str, milestones: &[i32], item: &str, _color: &str) -> String {
        let value = *self.stats.get(key).unwrap_or(&0);

        for &milestone in milestones {
            if value < milestone {
                return format!("{} {} {}", action, milestone, item);
            }
        }

        if value > 100 {
             return format!("Complete | {} {} {}", action, value, item);
        }

        format!("Quest {} Complete!\n{} Count: {}", action, action, value)
    }
}
