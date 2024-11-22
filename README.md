
# Snake Game in Python

This is a simple implementation of the classic Snake game using Pygame. The game features a grid-based movement system where the player controls a snake that grows longer each time it eats food. The objective is to eat as much food as possible without hitting the walls or itself.

## Features
- Grid-based movement.
- Growing snake when eating food.
- Game over condition when the snake hits the wall or itself.
- Win condition when all available cells are occupied by the snake.
- Simple and clean user interface.

## Requirements
- Python 3.8 or later.
- Pygame library.

## Installation

### Step 1: Clone the Repository
First, clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/snake_game_python.git
cd snake_game_python
```

### Step 2: Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies. You can create one using venv:
```bash
python3 -m venv venv
```

### Step 3: Activate the Virtual Environment
Activate the virtual environment based on your operating system:

On Windows:
```cmd
.\venv\Scripts\activate
```
On macOS and Linux:
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
With the virtual environment activated, install the required dependencies from requirements.txt:
```bash
pip install -r requirements.txt
```
Running the Game
Once the dependencies are installed, you can run the game using:
```bash
python main.py
```

## Controls
- Arrow Keys (Up, Down, Left, Right) to control the snake's direction.
- Enter to start a new game.

## Contributing
Contributions are welcome! If you have any ideas for improvements or bug fixes, feel free to open an issue or submit a pull request.