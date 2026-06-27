use console::style;

pub fn clear() {
    let term = console::Term::stdout();
    term.clear_screen().unwrap();
}

pub fn pause() {
    println!("\nPress any key to continue...");
    let term = console::Term::stdout();
    term.read_key().unwrap();
}

pub fn print_color(text: &str, color: &str) {
    match color {
        "green" => println!("{}", style(text).green()),
        "red" => println!("{}", style(text).red()),
        "blue" => println!("{}", style(text).blue()),
        "yellow" => println!("{}", style(text).yellow()),
        "cyan" => println!("{}", style(text).cyan()),
        "magenta" => println!("{}", style(text).magenta()),
        "bold_green" => println!("{}", style(text).green().bold()),
        "bold_red" => println!("{}", style(text).red().bold()),
        "bold_blue" => println!("{}", style(text).blue().bold()),
        "bold_yellow" => println!("{}", style(text).yellow().bold()),
        "bold_cyan" => println!("{}", style(text).cyan().bold()),
        "bold_magenta" => println!("{}", style(text).magenta().bold()),
        _ => println!("{}", text),
    }
}
