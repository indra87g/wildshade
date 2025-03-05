# Wildshade

[![wakatime](https://wakatime.com/badge/user/e3628b6b-08c8-497a-a679-c268fa16d35e/project/92acecd4-b82e-4476-b4b8-3030afc6c70f.svg)](https://wakatime.com/badge/user/e3628b6b-08c8-497a-a679-c268fa16d35e/project/92acecd4-b82e-4476-b4b8-3030afc6c70f)

A text-based survival game in Python, remake of [HSS](https://github.com/indra87g/hss)

## Getting Started
> WARNING: Current version of Wildshade is not a standalone binary. so, it need Python installed.

1. Clone this repository
```sh
git clone https://github.com/indra87g/wildshade.git
```

2. Install depedencies/tools
```sh
# recommended (install `uv` first!)
uv install
uv tool install tomlscript

# alternative
pip install click rich faker loguru
```

3. Run the game
```sh
# recommended
tomlscript run

# alternative
python main.py
```
