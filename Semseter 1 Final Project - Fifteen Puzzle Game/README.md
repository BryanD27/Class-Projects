# Description

Created for CS 5001 - Intensive Foundations of Computer Science, Northeastern University, Fall 2021

For the final project of my introductory Python course, I was tasked with recreating the classing Puzzle Game "Fifteen"
with Python's "Turtle" graphics module. Players are able to customize how their board looks, record their name on a 
leaderboard, and choose how many moves they're allowed before the game is over.

Project intended to display proficiency with lists, loops, file-reading, exception handling, and simple object oriented design.

# Instructions

1. Download folder "Semester 1 Final Project - Fifteen Puzzle Game" and keep all contents organized as they are within the directory

2. Within this folder, navigate to file "puzzle_game.py" and open it within IDLE (or any IDE you'd prefer)

3. Run the Python file, and enjoy the game!


# Design Notes

1. Use the "reset" button to automatically unscramble the puzzle. This is a "cheat code" of sorts in that the game still allows you 
to make moves that count towards your score even after this button is pressed. This was done intentionally, since the board
tiles are completely randomized and it is possible to be given an "unsolvable" board.

2. The "leaderboard" on the right is made solely to show proficiency in reading scores from a leaderboard file. It does not
take into account which puzzle the user solved or how many moves they allowed themselves.


3. All of the ".puz" files hold metadata that the Python program reads in order to determine the correct order of images that form an entire picture.
The "malformed" puz files are intentionally modified versions of the proper puz files, designed to correctly invoke an error message ("Could not find/open puz file").


