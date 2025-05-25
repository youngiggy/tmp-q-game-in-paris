# Paris Street Game

A pygame-based simulation of a classic street cup game in Paris. This game demonstrates the classic "shell game" scam where tourists often lose their money.

## Game Description

In this game, you play as a tourist in Paris who encounters a street game near the Eiffel Tower. The game consists of three scenes:

1. **Paris Square**: Navigate your character to find the street game among tourists.
2. **Game Introduction**: Watch as the vendor shows the ball and prepares the cups.
3. **The Cup Game**: Try to guess which cup contains the ball, but beware - the game is rigged!

## How to Play

- Use arrow keys to move your character in the Paris square
- Find the group of tourists to start the game
- Watch carefully as the cups are shuffled
- Place your bet on one of the available cups (not the one chosen by another tourist)
- Try to keep your money for as long as possible!

## Installation

### Local Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/paris-street-game.git
cd paris-street-game
```

2. Create a virtual environment and install dependencies:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pygame
```

3. Run the game:
```
python paris_game.py
```

## Web Deployment Options

### Option 1: Using Pygbag (Easiest)

[Pygbag](https://pygame-web.github.io/) allows you to run Pygame games in a web browser using WebAssembly.

1. Install pygbag:
```
pip install pygbag
```

2. Convert your game:
```
pygbag paris_game.py
```

3. This creates a build in the `build/web` directory that you can upload to any web hosting service.

### Option 2: Using Replit

1. Create an account on [Replit](https://replit.com/)
2. Create a new Python repl
3. Upload your game files
4. Install pygame in the Replit package manager
5. Run the game and share the link

### Option 3: GitHub Pages with Pygbag

1. Push your code to a GitHub repository
2. Set up GitHub Actions to build your game with pygbag
3. Enable GitHub Pages to serve the built files

## Credits

Created by [Your Name]

## License

This project is licensed under the MIT License - see the LICENSE file for details.
