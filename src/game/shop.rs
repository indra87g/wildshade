use crate::game::data::items_for_sale;
use crate::game::player::Player;
use crate::utils::ui::print_color;
use crate::utils::logger::log_warning;
use std::collections::HashMap;

pub struct Shop {
    pub items_for_sale: HashMap<String, i32>,
    pub sell_prices: HashMap<String, i32>,
}

impl Shop {
    pub fn new() -> Self {
        let items = items_for_sale();
        let mut sell_prices = HashMap::new();
        for (item, price) in &items {
            sell_prices.insert(item.clone(), price / 2);
        }
        Self {
            items_for_sale: items,
            sell_prices,
        }
    }

    pub fn show_shop(&self) {
        println!("--- Shop ---");
        for (item, price) in &self.items_for_sale {
            println!("{}: {}c", item, price);
        }
        println!("------------");
    }

    pub fn buy(&self, player: &mut Player, item: &str) {
        if let Some(&price) = self.items_for_sale.get(item) {
            if player.coins >= price as f64 {
                print_color(&format!("You bought {} for {}", item, price), "green");
                player.inventory.add_item(item, 1);
                player.coins -= price as f64;
            } else {
                print_color(&format!("Not enough coins to buy {}", item), "red");
            }
        } else {
            print_color(&format!("{} is not found in the shop", item), "red");
            log_warning(&format!("'{}' is not found in 'items_for_sale'.", item));
        }
    }

    pub fn sell(&self, player: &mut Player, item: &str) {
        if player.inventory.items.contains_key(item) {
            let price = *self.sell_prices.get(item).unwrap_or(&0);
            player.inventory.remove_item(item, 1);
            player.coins += price as f64;
            print_color(&format!("You sold {} for {}c", item, price), "green");
            print_color(&format!("Your current coins: {}c", player.coins), "blue");
        } else {
            print_color(&format!("You don't have {} to sell", item), "red");
        }
    }
}
