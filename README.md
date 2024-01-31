# IFT1015-TP2 - Python Minesweeper Game

This project is a Python-based implementation of the classic Minesweeper game, with a unique twist. It utilizes the [Codeboot](https://codeboot.org/) Python interpreter, developed by a student at the Université de Montréal, and incorporates web technologies such as HTML and CSS for the user interface. The game challenges players to clear a rectangular board containing hidden "mines" without detonating any of them, using clues about the number of neighboring mines in each field.

## Features

- **Customizable Board Size:** Players can define the width and height of the minesweeper grid to increase or decrease the difficulty level.
- **Dynamic Bomb Placement:** Bombs are randomly placed on the board, ensuring a unique experience for every game.
- **Recursive Unveiling:** Implements a breadth-first search (BFS) algorithm to recursively unveil adjacent cells, providing a seamless gameplay experience.
- **Flagging Option:** Players can flag suspected mines to avoid accidental clicks, enhancing strategic gameplay.
- **End-Game Detection:** The game automatically detects a win or loss, providing appropriate feedback to the player.

## Technologies Used

- **Python:** Core game logic and event handling.
- **HTML & CSS:** User interface and styling.
- **Codeboot Interpreter:** A Python interpreter that allows for seamless integration of Python code with web technologies.
- **Breadth-First Search (BFS) & Recursivity:** For unveiling adjacent cells and implementing game logic.

## How to Play

1. **Start the Game:** Initialize the game by specifying the desired grid size.
2. **Left Click:** Unveil a cell. If the cell is a mine, the game ends. Otherwise, the cell shows either the number of adjacent mines or a blank space, unveiling more of the board.
3. **Shift + Left Click:** Place or remove a flag on a cell to mark it as a suspected mine.
4. **Winning the Game:** The game is won by unveiling all cells without mines.

## Contributing

Contributions to the project are welcome! If you have suggestions for improvements or bug fixes, feel free to open an issue or submit a pull request.

## Acknowledgments

Special thanks Mr. Marc Feeley, professor who give this programming course and this amazing project

