mod game;
mod utils;

use game::player::Player;
use game::shop::Shop;
use game::data::get_fake_name;
use utils::ui::{clear, pause, print_color};
use utils::logger;
use inquire::{Select, Text, CustomType};

fn welcome() -> Player {
    print_color("Welcome to Wildshade!", "bold_cyan");
    pause();
    clear();

    let name = Text::new("Enter your name:").prompt().unwrap();
    let player_name = if name.trim().is_empty() {
        logger::log_warning("'name' is not provided, using fake name instead.");
        get_fake_name()
    } else {
        name
    };

    Player::new(player_name)
}

fn explore_menu(player: &mut Player) {
    clear();
    print_color("What would you like to do?", "bold_blue");
    let options = vec!["Explore", "Quest", "Back"];
    let action = Select::new("Action:", options).prompt().unwrap();

    match action {
        "Explore" => {
            player.explore();
            pause();
        }
        "Quest" => {
            player.quest.show_quest();
            pause();
        }
        "Back" => return,
        _ => unreachable!(),
    }
}

fn consume_menu(player: &mut Player) {
    clear();
    print_color("What would you like to do?", "bold_blue");
    let options = vec!["Eat", "Drink", "Back"];
    let action = Select::new("Action:", options).prompt().unwrap();

    match action {
        "Eat" => {
            let food = Text::new("Enter food name to eat:").prompt().unwrap();
            player.eat(&food);
            pause();
        }
        "Drink" => {
            player.drink();
            pause();
        }
        "Back" => return,
        _ => unreachable!(),
    }
}

fn work_menu(player: &mut Player) {
    clear();
    print_color("What would you like to do?", "bold_blue");
    let options = vec!["Mining", "Woodcutting", "Back"];
    let action = Select::new("Action:", options).prompt().unwrap();

    match action {
        "Mining" => {
            let hours = CustomType::<i32>::new("How many hours do you want to mine?").prompt().unwrap();
            player.mining(hours);
            pause();
        }
        "Woodcutting" => {
            print_color("Woodcutting is not implemented yet!", "yellow");
            pause();
        }
        "Back" => return,
        _ => unreachable!(),
    }
}

fn shop_menu(player: &mut Player) {
    clear();
    let shop = Shop::new();
    shop.show_shop();
    print_color("What would you like to do?", "bold_blue");
    let options = vec!["Buy", "Sell", "Back"];
    let action = Select::new("Action:", options).prompt().unwrap();

    match action {
        "Buy" => {
            let item = Text::new("Enter item name to buy:").prompt().unwrap();
            shop.buy(player, &item);
            pause();
        }
        "Sell" => {
            let item = Text::new("Enter item name to sell:").prompt().unwrap();
            shop.sell(player, &item);
            pause();
        }
        "Back" => return,
        _ => unreachable!(),
    }
}

fn main() {
    logger::init();
    logger::log_info("Program started");

    let mut player = Player::new(get_fake_name());
    player.load_game("savegame.json");

    if player.savegame_notfound {
        player = welcome();
    }

    loop {
        clear();
        player.show_status();

        if !player.check_status() {
            println!("Game Over!");
            break;
        }

        print_color("What would you like to do?", "bold_blue");
        let options = vec!["Explore", "Consume", "Work", "Rest", "Inventory", "Shop", "Save", "Load", "Quit"];
        let action = Select::new("Action:", options).prompt().unwrap();

        match action {
            "Explore" => explore_menu(&mut player),
            "Consume" => consume_menu(&mut player),
            "Work" => work_menu(&mut player),
            "Rest" => {
                let hours = CustomType::<i32>::new("How many hours do you want to sleep?").prompt().unwrap();
                player.rest(hours);
                pause();
            }
            "Inventory" => {
                player.inventory.show_inventory();
                pause();
            }
            "Shop" => shop_menu(&mut player),
            "Save" => {
                player.save_game("savegame.json");
                pause();
            }
            "Load" => {
                player.load_game("savegame.json");
                pause();
            }
            "Quit" => {
                player.save_game("savegame.json");
                clear();
                print_color("Thanks for playing! Come back soon!", "bold_red");
                logger::log_info("Program closed securely.");
                break;
            }
            _ => unreachable!(),
        }
    }
}
