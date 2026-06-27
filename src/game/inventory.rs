use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use crate::utils::ui::print_color;

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Inventory {
    pub items: HashMap<String, i32>,
}

impl Inventory {
    pub fn new() -> Self {
        Self {
            items: HashMap::new(),
        }
    }

    pub fn add_item(&mut self, item: &str, quantity: i32) {
        let count = self.items.entry(item.to_string()).or_insert(0);
        *count += quantity;
        print_color(&format!("Added {}x {} to inventory.", quantity, item), "green");
    }

    pub fn remove_item(&mut self, item: &str, quantity: i32) {
        if let Some(count) = self.items.get_mut(item) {
            if *count > quantity {
                *count -= quantity;
                print_color(&format!("Removed {}x {} from inventory.", quantity, item), "yellow");
            } else {
                self.items.remove(item);
                print_color(&format!("{} removed from inventory.", item), "red");
            }
        } else {
            print_color(&format!("{} not found in inventory.", item), "red");
        }
    }

    pub fn show_inventory(&self) {
        if self.items.is_empty() {
            print_color("Your inventory is empty.", "red");
            return;
        }

        println!("--- Inventory ---");
        for (item, quantity) in &self.items {
            println!("{}: {}", item, quantity);
        }
        println!("-----------------");
    }
}
