'''
Bryan Dumond
CS 5001 - Fall 2021
Final Project - 15 Sliding Puzzle Game

A Python version of the classic "15-Slider" game, with different loadable boards,
a leaderboard, and the ability to "cheat" by having the game automatically unscramble
with the press of a button! Meant to show off proficiency with Classes, lists, dictionaries,
and functions.
'''

import turtle, random, os
from datetime import datetime


'''
Constants -- All constants used throughout the program stored here
'''

SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1000

TILE_MARGIN = 7
TILE_BORDER = 5
TILE_START_X = -385
TILE_START_Y = 325

TILE_MIN_SIZE = 50
TILE_MAX_SIZE = 110

VALID_BOARD_SIZES = [4, 9, 16]

THUMB_X = 390
THUMB_Y = 400

LOWER_MOVE_BOUND = 5
UPPER_MOVE_BOUND = 200

SPLASH_TIMER = 4000  # milliseconds

MSG_TIMER = 5000

WARNING = 3

'''
Classes - Two classes total used for this program: Board and Tile.
'''

class Tile:
    '''
    Class --- This class handles everything related to the appearance and
        data about particular tiles. Tiles can draw themselves, store
        their location in both Turtle and a nested list, tell whether
        or not its blank, etc.
    '''

    def __init__(self, address, number):
        '''
        Attributes -- takes in a file path address and a number (int).
            The address will be used to get the image to be drawn, and
            the number is used to name the Tile to make it easier track
            in the IDLE shell.
        '''
    
        self.address = address
        self.name = f"Tile {number}"
        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()

    def is_blank(self):
        '''
        Method --- Returns a boolean (bool) telling user whether
            or not this tile is the blank one
        '''
        
        temp_string = self.address[-1:-10:-1]
        temp_string_reversed = temp_string[::-1]
            
        if temp_string_reversed == "blank.gif":
            return True
        else:
            return False
            
    def set_coordinates(self, x_y_tuple):
        '''
        Method --- Saves a tuple of the x,y coordinate where
            this tile is currently drawn on screen
        '''
        self.coordinates = x_y_tuple
        self.x = self.coordinates[0]
        self.y = self.coordinates[1]

    def stored_cell_number(self, cell):
        '''
         Method --- saves the cell number on the board where
            tile is currently located
        '''
        self.cell = cell

    def location_in_list(self, row, column):
        '''
        Method -- saves the i,j index of Tile's location in the
            Board class' nested list of all tiles on the board.
        '''
        self.index_r = row
        self.index_c = column
            
    def draw(self):
        '''
        Method -- draws Tile image to the screen
        '''
     
        self.turtle.speed(0)
        self.turtle.shape(self.address)
        self.turtle.penup()
        self.turtle.goto(self.coordinates)
        self.turtle.showturtle()
  
        self.turtle.onclick(self.process_click)

        
    def process_click(self, x, y):
        '''
        Callback --- Allows Tile objects to be clicked on, which
            activates the Board class' switch_tiles method.
        '''

        global game_board
            
        print(f"You clicked on {self.name} at Cell {self.cell}")
        print(f"Nested List Index: [{self.index_r}] [{self.index_c}]")
        if self.is_blank() == True:
            print("This is the blank")
        print("")
        return game_board.switch_tiles(self)
        

    def __str__(self):
        return self.name

    def __eq__(self, other):
        '''
        EQ Method -- Determines that two Tile objects are equal if they
            have the same file path image to be drawn. Returns a boolean
            (bool) determining whether this is true.
        '''    
        if self.address == other.address:
            return True
        else:
            return False


class Board:
    '''
    Class --- The main processor of everything that happens on the 16-cell
        game board itself. Knows how to process .puz file data, draw cells,
        move Tiles, shuffle the board, draw to the screen, update score,
        solve the puzzle, and much more
    '''

    def __init__(self, address, move_limit):
        '''
        Init -- Takes in the address of the puz file that will be used
            to create a game board. Also the given move limit specificed
            by the user in order to check win states
        '''

        dictionary = generate_dict(address)

        self.name = dictionary["name"]
        self.number = int(dictionary["number"])

        # Directory info for puz / images to be used
        self.current_dir = os.listdir()
        self.images_dir = os.listdir("Images")
        
        self.size = int(dictionary["size"])
        self.thumb_address = dictionary["thumbnail"]
    
        self.columns = int(self.number ** 0.5)
        self.rows = self.columns  # Because it's a square

        self.player_moves = 0
        self.move_limit = move_limit
        self.moves_left = self.move_limit - self.player_moves

        
        self.tile_list = []
        for i in range(self.number):
            tile = Tile(dictionary[str(i+1)], i + 1)
            self.tile_list.append(tile)

        self.address_list = []
        for i in range(self.number):
            address = self.tile_list[i].address
            self.address_list.append(address)
        self.address_list.append(self.thumb_address)
        


        self.valid = self.validate_puzz_file()

        if self.valid == True:
            self.setup_new_board()
        
    def setup_new_board(self):
        '''
        Helper Method -- convenient way to launch all of the 
            board setup functions once the .puz is validated
        '''
        
        self.load_tiles()
        self.draw_cells()
        self.create_solved_board()
        self.create_shuffled_board()
        self.draw_board_tiles()
        self.draw_thumbnail()
        self.display_current_score()


    def validate_puzz_file(self):
        '''
        Method -- checks validity of metadata in current .puz file.
            Checks whether its file paths exist, and also whether
            its number & size are within the given constraints.
          Returns -- valid -- a boolean (bool) determining whether
            or not the .puz metadata is valid.
        '''
        
        if self.number not in VALID_BOARD_SIZES:
            error = f"Tile Numbers '{self.number}' is invalid "                                       
            valid = False
        
        elif self.size < TILE_MIN_SIZE or self.size > TILE_MAX_SIZE:
            error = f"Tile Size '{self.size}' is invalid"                                        
            valid = False

        elif self.name not in self.images_dir:
            error = f"Image directory '{self.name}' does not exist"
            valid = False

        elif self.check_file_paths() != None:
            valid = False
            error = f"'{self.check_file_paths()}' path does not exist"
        else:
            valid = True
            
        if valid == False:
            error_msg = str(datetime.now()) + (f" Error: {error} | LOCATION" +
                                    " game_board.validate_puzz_file()")
            invalid_board(error_msg)
            
        return valid

    def check_file_paths(self):
        '''
        Method -- checks whether the list of file paths generated at init
            from .puz file are valid file paths in current directory
          Returns -- address -- if a bad file path (str) is found, it is
             returned to the validate function so that it can be error logged
        '''

        # Get string lists of all file paths that the board will use
        curr_dir = os.listdir()
        img_dir = os.listdir("Images")
        tile_dir = os.listdir(f"Images/{self.name}")

        # Find the indices that reveal folder holding tile images
        ind1 = curr_dir.index("Images")
        ind2 = img_dir.index(f"{self.name}")

        # Build list of all potential file paths of that folder
        curr_addresses = []
        for i in range(len(tile_dir)):
            tile_str = f"{curr_dir[ind1]}/{img_dir[ind2]}/{tile_dir[i]}"
            curr_addresses.append(tile_str)

        # Check to see if all puz file addresses are in actual file path list
        for address in self.address_list:
            if address in curr_addresses:
                continue
            else:
                return address      
        return None
        

    def load_tiles(self):
        '''
        Method -- adds tile images to Screen's shape library
        '''
        global screen
        for each in self.tile_list:
            screen.addshape(each.address)

    def create_solved_board(self):
        '''
        Method -- creates a separate nested list of Tile objects
            representing the winning configuration. Current board (represented
            by another nested list) will be compared to this
        '''

        self.solved_board = []
        for i in range(self.rows):
            temp_list = []
            for j in range(self.columns):
                tile = self.tile_list[(i * self.columns) + j]
                temp_list.append(tile)
            self.solved_board.append(temp_list)
                    
    def solve_board(self):
        '''
        Method -- solves the current nested list game board (invoked by pressing
            the reset button on Turtle screen) 
        '''

        for i in range(self.rows):
            for j in range(self.columns):
                self.board[i][j] = self.tile_list[(i * self.columns) + j]

        self.set_tile_data()
        
    
    def create_shuffled_board(self):
        '''
        Method -- creates the initial game board list whenever a new .puz
            file is loaded. It is a nested list representing what a 2D grid
            would look like
        '''

        shuffled_indices = create_shuffled_indices(self.tile_list)

        self.board = []
        for i in range(self.rows):
            temp_list = []
            for j in range(self.columns):
                tile = self.tile_list[shuffled_indices.pop()]
                temp_list.append(tile)
            self.board.append(temp_list)

        self.set_tile_data()

    def draw_cells(self):
        '''
        Method -- draws the outlines of where tiles will be placed, while also
            saving those coordinate points in a list that will be used to place
            tiles onto the board. Draws from top left to bottom right of grid.
        '''
             
        self.outline = turtle.Turtle()
        self.outline.speed(0)
        self.outline.hideturtle()
        self.outline.penup()
        self.outline.goto(TILE_START_X, TILE_START_Y)

        self.cell_coordinates = []
        
        for i in range(self.rows): # Number of Rows
            for j in range(self.columns): # Columns/Elements per row

                # Draw Square
                self.outline.pendown()
                self.outline.width(TILE_BORDER)
                for k in range(4):
                    self.outline.forward(self.size)
                    self.outline.right(90)

                # Relocate to square middle
                self.outline.penup()
                self.outline.forward(self.size/2)
                self.outline.right(90)
                self.outline.forward(self.size/2)
                self.outline.left(90)

                # store cell coordinates
                cell_coordinate = (self.outline.xcor(), self.outline.ycor())
                self.cell_coordinates.append(cell_coordinate)
                
                # Relocate to beginning position of next square 
                self.outline.forward(self.size/2)
                self.outline.left(90)
                self.outline.forward(self.size/2)
                self.outline.right(90)
                self.outline.forward(TILE_MARGIN)

            # Relocate to next row beginning
            self.outline.goto(TILE_START_X,
                              TILE_START_Y - (self.size + TILE_MARGIN)*(i+1))

    
    def draw_updated_board(self, tile_1, tile_2):
        '''
        Method -- After a Tile switch is deemed valid on self.board, this function
            tells each tile to redraw itself at its new saved location. Score is
            also re-drawn to reflect update.
          Parameters -- tile_1, tile_2 -- two Tile objects whose turtle objects
             will be used to redraw their new positions on screen.
        '''
        # Update Tiles
        switched_tiles = tile_1, tile_2

        for each in switched_tiles:
            each.turtle.showturtle()
            each.turtle.goto(each.coordinates)

        # Update Text
        self.moves_made_display.clear()
        self.moves_made_display.write(f"Moves Made: {self.player_moves} ",
                                      move = False, align = "left",
                                      font=('Arial', 24, 'normal'))
        self.moves_left_display.clear()

        # Display moves left in red to signal player
        if self.moves_left <= WARNING:
            self.moves_left_display.color('red')
            self.moves_left_display.write(f"Moves Left: {self.moves_left}",
                                          move = False, align = "left",
                                          font=('Arial', 26, 'bold'))
        else:
            self.moves_left_display.write(f"Moves Left: {self.moves_left} ",
                                          move = False, align = "left",
                                          font=('Arial', 26, 'normal'))

            
    def display_current_score(self):
        '''
        Method -- draws initial text to screen representing how many moves
            a player has made and how many they have left before the program
            terminates
        '''

        self.moves_left_display = turtle.Turtle()

        self.moves_left_display.penup()
        self.moves_left_display.hideturtle()
        self.moves_left_display.speed(0)
        self.moves_left_display.goto(-350, -365)
        self.moves_left_display.write(f"Moves Left: {self.moves_left} ",
                                      move = False, align = "left",
                                      font=('Arial', 26, 'normal'))

        self.moves_made_display = turtle.Turtle()

        self.moves_made_display.penup()
        self.moves_made_display.hideturtle()
        self.moves_made_display.speed(0)
        self.moves_made_display.goto(-350, -405)
        self.moves_made_display.write(f"Moves Made: {self.player_moves} ",
                                      move = False, align = "left",
                                      font=('Arial', 26, 'normal'))    

    def draw_board_tiles(self):
        '''
        Method -- Tells Tile objects to draw themselves in the coordinates
            that they have saved after board shuffle. Should appear on screen
            in "random" order (it is just the order that the tiles are listed
            in the .puz file)
        '''
        
        # Tiles drawn in "random" order is visually fitting for puzzle game
        for i in range(len(self.tile_list)):
            tile = self.tile_list[i]
            tile.draw()


    def set_tile_data(self):
        '''
        Method -- Assigns cell numbers and nested list indices
            to the Tile objects on the shuffled board (nested list)
        '''
        for i in range(self.rows):
            for j in range(self.columns):
                tile = self.board[i][j]
                tile.set_coordinates(self.cell_coordinates[(i * self.rows)
                                                           + j])
                tile.stored_cell_number(i * self.rows + j)
                tile.location_in_list(i,j)

        
    def switch_tiles(self, tile):
        '''
        Method -- Invoked by clicking on a Tile object on the Turtle screen.
            If move is valid, Tile object indexes on self.board list are
            updated, and functions are called to both change the Tile object
            metadata, update teh score, re-draw the screen, and check
            for a win/loss.
          Parameter -- tile -- A Tile Object that was clicked and will be
            compared to a blank tile.
        '''

        clicked_row = tile.index_r
        clicked_column = tile.index_c
        clicked_index = (clicked_row, clicked_column)

        blank = self.find_blank_tile()
        blank_index = (blank.index_r, blank.index_c)

        if self.check_valid_switch(clicked_index , blank_index) == True:
            
            switched_out = self.board[blank.index_r][blank.index_c]
            
            self.board[blank.index_r][blank.index_c] = tile
            self.board[clicked_row][clicked_column] = switched_out

            self.update_switched_tile_data(tile, switched_out)

            self.player_moves += 1
            self.moves_left -= 1

            self.draw_updated_board(tile, switched_out)
            
            self.check_end()

    def check_valid_switch(self, clicked_index, blank_index):
        '''
        Method -- Analyzes the index locations of the clicked
            and the blank tiles on the nested list board to
            see whether a switch is valid. Returns a boolean
            (bool) with result.
          Returns -- boolean (True/False) 
        '''
        
        # If tiles in the same row and adjacent columns
        if abs(clicked_index[0] - blank_index[0]) == 0 and \
            abs(clicked_index[1] - blank_index[1]) == 1:
                return True

        # If in the same column and adjacent rows
        elif abs(clicked_index[1] - blank_index[1]) == 0 and \
            abs(clicked_index[0] - blank_index[0]) == 1:
                return True
        else:
            return False

    def check_end(self):
        '''
        Method -- Checks the win/loss conditions of the game
            If a round over is valid, sends the player score
            to the end_round function
        '''
        global screen
        
        if self.player_moves == self.move_limit:
            if self.board != self.solved_board:
                print("You lose!")
                end_round(False, self.player_moves)
            else:
                print("You win!")
                end_round(True, self.player_moves)
                
        elif self.board == self.solved_board:
            print("You win!")
            end_round(True, self.player_moves)
        

    def find_blank_tile(self):
        '''
        Method -- searches the nested list board for the
            Tile containing the metadata for being blank.
            Tile object is returned if True
          Return -- Tile object that holds the blank tile
            data in the nested list board.
        '''
        
        for row in self.board:
            for tile in row:
                if tile.is_blank() == True:
                    return tile
    
    def update_switched_tile_data(self, tile_1, tile_2):
        '''
        Method -- Switches stored metadata of two Tile
            objects after a valid switch has been performed.
            The nested list board is not modified: only the
            data of the Tile objects it holds is.
          Parameters -- tile_1, tile_2 -- Two Tile objects
            that are going to have their stored data updated
        '''
        
        temp_cell = tile_1.cell
        temp_coord = tile_1.coordinates
        temp_i_r = tile_1.index_r
        temp_i_c = tile_1.index_c

        tile_1.cell = tile_2.cell
        tile_1.coordinates = tile_2.coordinates
        tile_1.index_r = tile_2.index_r
        tile_1.index_c = tile_2.index_c

        tile_2.cell = temp_cell
        tile_2.coordinates = temp_coord
        tile_2.index_r = temp_i_r
        tile_2.index_c = temp_i_c
          
    def draw_thumbnail(self):
        '''
        Method -- Draws the thumbnail to top right of the screen after
            obtaining its metadata from .puz file
        '''
        
        self.thumb = place_image(self.thumb_address, THUMB_X, THUMB_Y)


    def reset_board(self):
        '''
        Method -- Invoked by pressing the Reset button on the Turtle Screen.
            Modifies the nested list board object to have all its Tiles be
            in solved orientation, and then calls the draw_board_tiles
            function to let Tiles draw their new locations on screen
        '''
        try:
            self.solve_board()
            self.draw_board_tiles()
            
        # If user tries to "reset" an empty screen, do nothing
        except AttributeError:
            pass

    def erase_board(self):
        '''
        Method -- Hides the turtles of all Tile objects and the thumnbail
            on screen, and erases Tile outlines and score display
        '''
        for i in range(len(self.tile_list)):
            tile = self.tile_list[i]
            tile.turtle.hideturtle()
            
        self.thumb.hideturtle()
        self.outline.clear()
        self.moves_made_display.clear()
        self.moves_left_display.clear()        
            

'''
General Functions - These are functions outside of the Game and Tile classes that
        deal with logic outside of the tile boeard itself.
'''

def generate_dict(address):
    '''
    Function -- Reads in a .puz file and organizes its data into a dictionary
            (dict) that is passed into a Board object for processing
        Parameters -- A str representing a file path
        Returns -- a puzzle dictionary (dict)
    '''
    puzzle_dict = {}
    
    with open(address, mode = 'r') as puzzle_data:
        for line in puzzle_data:
            temp_puz_list = line.split(": ")
                
            puzzle_dict[temp_puz_list[0]] = temp_puz_list[1].strip("\n")
    return puzzle_dict

        
def create_shuffled_indices(lst):
    '''
    Function -- Creates a list (list) of numbers from 0 to the length of
            list that is passed in in random order, and returns it to sender
        Parameters - A list of objects
        Returns - A list of shuffled integers (int)
    '''
    
    shuffled_indices = []

    index = random.randint(0, len(lst) - 1)

    while len(shuffled_indices) != len(lst):
        if index not in shuffled_indices:
            shuffled_indices.append(index)

        else:
            # repeats get reshuffled
            index = random.randint(0, len(lst) -1) 
    return shuffled_indices
    
  
def draw_outlines(x, y, thickness, color, length, width):
    '''
    Function -- Draws the large thick rectangle outlines surrounding the play area,
            leaderboard area, and status area
        Parameters -- x - int representing x coordinate of where to draw
                      y - int representing y coordinate of wher eto draw
                      thickness - int from 1-10 describing desired line width.
                      color - string (str) of the color of the line to be drawn
                      length - int representing how many units one side should be
                      width - int representing how many unites other side should be
    '''
    outline = turtle.Turtle()
    outline.speed(0)
    outline.hideturtle()

    outline.penup()
    outline.goto(x,y)
    outline.pensize(thickness)
    outline.color(color)
    outline.pendown()
    
    for i in range(2):
        outline.forward(length)
        outline.right(90)
        outline.forward(width)
        outline.right(90) 

    
def create_status_buttons():
    '''
    Function -- Creates the three buttons (quit, load, reset) by
        calling the functions to place them on the screen
        and make them clickable
    '''

    quit_address = "Resources/quitbutton.gif"
    load_address = "Resources/loadbutton.gif"
    reset_address = "Resources/resetbutton.gif"

    quit_button = place_image(quit_address, 350, -375)
    load_button = place_image(load_address, 200, -375)
    reset_button = place_image(reset_address, 50, -375)

    quit_button.onclick(press_quit)
    load_button.onclick(press_load)
    reset_button.onclick(press_reset)
    

def press_quit(x,y):
    '''
    Callback Function -- Invoked by clicking the Quit button. Clears
        entire screen, displays quit message, and calls the end_game
        function
    '''
    
    global screen
    
    print("Clicked Quit\n")

    screen.clearscreen()
    
    screen.addshape("Resources/quitmsg.gif")
    quit_msg = turtle.Turtle()
    quit_msg.shape("Resources/quitmsg.gif")

    screen.ontimer(end_game, t = MSG_TIMER)

def press_reset(x,y):
    '''
    Callback Function -- Invoked by clicking Reset button.
        Returns -- Tells game_board object to call reset_board method
    '''
    
    print("Clicked Reset\n")
    return game_board.reset_board()


def press_load(x,y):
    '''
    Callback Function -- Invoked by pressing Load button
        Returns -- Calls load_new_board() function
    '''
    print("Clicked Load\n")
    return load_new_board()


def load_new_board():
    '''
    Function -- Checks the current directory to see if the user
        selected .puz file is valid. If so it erases the current
        game board (if there is one) and creates the new instance
        of the Board object
    '''

    global game_board
    global move_limit

    contents = os.listdir()
    puzz_file_names = []
    
    for each in contents:
        if each[-1:-5:-1] == ".puz"[::-1]:
            each += "\n"
            puzz_file_names.append(each)

    files_string = "".join(puzz_file_names)

    
    new_board = screen.textinput("Load Puzzle",
                                "Which board would you like to load?\n"
                                f"Choices are:\n\n{files_string}")
    try:
        if new_board + "\n" in puzz_file_names:
            
            # If board is already erased, go straigth to exception
            try:
                game_board.erase_board()
                game_board = Board(new_board, move_limit)
            except AttributeError:
                game_board = Board(new_board, move_limit)
        else:
            time_stamp = datetime.now()
            error = str(time_stamp) + (f" Error: File '{new_board}' not found" +
                                           " | LOCATION: load_new_board()")
            invalid_board(error)
    except TypeError:
        
        # If the user presses cancel, just go back to the game
        pass
    
def place_image (address, x, y):
    '''
    Function -- Takes in an file path for an image and x,y coordinate,
            creates a Turtle to hold them and draws them at the specified
            location. Also returns the created Turtle
        Parameters -- address = string representing a file path
                      x = int for x coordinate
                      y = int for y coordinate
        Returns -- The Turtle Object used to draw the image
    '''
    global screen
    
    screen.addshape(address)
    image = turtle.Turtle()
    image.hideturtle()
    image.speed(0)
    image.shape(address)
    image.penup()
    image.goto(x, y)
    image.showturtle()
    
    return image


def get_leaderboard():
    '''
    Function -- Opens the leaderboard file and reads data into lists with lengths of
            two (one int for score and one str for name), which are then nested into
            one bigger list that will be sorted and printed to the screen. If leaderboard
            not found, sends error data to error logger function.
        Returns -- The nest list of leaderboard data (0 = int, 1 = str)
    '''
    
    global screen

    leaderboard_list = []
    
    def dismiss_message(x,y):
        return leaderboard_error.hideturtle()

    try:
        with open('leaderboard.txt', 'r') as leaderboard_file:
            for entry in leaderboard_file:
                temp_leaderboard_list = entry.split(' : ')
                temp_leaderboard_list[0] = int(temp_leaderboard_list[0])
                temp_leaderboard_list[1] = temp_leaderboard_list[1].strip("\n")
                leaderboard_list.append(temp_leaderboard_list)

    except FileNotFoundError:
        screen.addshape("Resources/leaderboard_error.gif")
        leaderboard_error = turtle.Turtle()
        leaderboard_error.shape("Resources/leaderboard_error.gif")
        
        leaderboard_error.showturtle()
        
        # Send error to the err file
        time_stamp = datetime.now()
        error_msg = str(time_stamp) +(f" Error: File 'leaderboard.txt'"
                        " not found" + " | LOCATION: get_leaderboard()")
        screen.onscreenclick(dismiss_message)
        error_logger(error_msg)

    return leaderboard_list


def edit_leaderboard(player, score):
    '''
    Function -- Takes in a player name (str) and score (int) from a player who won
            and appends it to the leaderboard text file.
        Parameters -- player_name (str) and player score (int)
    '''
    with open('leaderboard.txt', 'a') as leaderboard_file:
        leaderboard_file.write(f"{score} : {player}\n")

    print(f"Added {player} to leaderboard")


def sort_leaderboard(leaderboard : list):
    '''
    Function -- Takes in the nested list of leaderboards and sorts them
            in order from smallest score (int, 0 index of each nested list)
            to highest score. Returns to sender
        Returns -- A modified nested list (lst) of ints (at the nested 0)
                and strings (at the nested 1) in numerical order of the first
                index of every nested list (smallest to largest)
        Ex: [7, "Nancy"], [3, "Sean"] --> [[3, "Sean"], [7, "Nancy"]]
    '''
    leaderboard.sort(key = lambda x: x[0])
    return leaderboard
    

def display_leaderboard(sorted_lb):
    '''
    Function -- Creates a Turtle that draws to the screen the Leaderboard header
            category titles, and also reads from the passed in sorted leaderboard list
            and draws them to the screen in order.
        Parameters -- sorted_lb -- a nested list (each nest being a list of score (int,
            index 0) and player (str, index 1)
    '''
    title = turtle.Turtle()
    title.speed(0)
    title.hideturtle()

    title.color("blue")
    title.penup()
    title.goto(160, 380)
    title.write("LEADERS ",
                move = False, align = "left",
                font=('Arial', 28, 'bold'))

    title.goto(145, 305)
    title.write("#    Player  Score", move = False, align = "left",
                font=('Courier', 22, 'bold'))
    title.goto(145, 270)
    title.setheading(270)

    placement = 0

    # For aesthetics/clarity, only display the Top 18 on Leaderboard
    short_lb_list = sorted_lb[:17]

    for i in range(len(short_lb_list)):
        if i > 0 and sorted_lb[i-1][0] == sorted_lb[i][0]:
            placement += 0
        else:
            placement += 1
        score = sorted_lb[i][0]
        player = sorted_lb[i][1]
        title.write(f"{placement}\t{player} \t{score}",
                    move = False, align = "left", font = ('Arial', 20, 'normal'))
        title.forward(30)
    
        
def end_round(winner, score):
    '''
    Function -- Is passed in a boolean (bool) which it uses to display either the
            win or lose message, and also score that is used to draw to the screen
            with the turtle it creates. Also invokes function that sends winning
            scores to leaderboard. If player scored higher than the previous high,
            big green letters show that they have a new high score.
        Parameters -- winner, score -- winner is a boolean determining whether the
                player has won or lost, and score is an int. Lower score = better.
    '''
    global screen
    global player_name
    global score_to_beat
    
    screen.clearscreen()
    
    win_lose_message = turtle.Turtle()
    win_lose_message.hideturtle()

    if winner == True:
        screen.addshape("Resources/winner.gif")
        win_lose_message.shape("Resources/winner.gif")
        win_lose_message.showturtle()

        # send name, score to be written on the leaderboard
        edit_leaderboard(player_name, score)
        
    elif winner == False:
        screen.addshape("Resources/Lose.gif")
        win_lose_message.shape("Resources/Lose.gif")
        win_lose_message.showturtle()

    result_text = turtle.Turtle()
    result_text.hideturtle()
    result_text.penup()
    result_text.color("purple")
    result_text.goto(0, -185)
    
    result_text.write(f"     Player: {player_name}\n Score: {score} Moves"
                      ,move = False, align = "center",
                     font=('Arial', 32, 'bold'))
    if winner == True:
        if score < score_to_beat:
            print("New High Score!")
            result_text.goto(0, -300)
            result_text.color("green")
            result_text.write("NEW HIGH SCORE!", move = False,
                              align = "center", font = ('Arial', 36, 'bold'))      
    screen.ontimer(end_game, t = MSG_TIMER)

    
def end_game():
    '''
    Function -- Clears the screen and shows the Credit image to the viewer.
        Clicking anywhere on the screen will close the Turtle graphics
        module and end the game for good
    '''
    global screen

    screen.clearscreen()
    
    screen.addshape("Resources/credits.gif")

    end_credits = turtle.Turtle()
    end_credits.shape("Resources/credits.gif")
    end_credits.showturtle()

    exit_text = turtle.Turtle()
    exit_text.hideturtle()
    exit_text.penup()
    exit_text.goto(0, -360)
    exit_text.write("    Thanks for playing!\nClick Anywhere to Exit ",
                move = False, align = "center",
                font=('Arial', 28, 'bold'))
    
    screen.exitonclick()


def invalid_board(error_msg):
    '''
    Function -- displays the "file error" message to the player when there
            is an issue reading/finding the .puz file from the "Load" button.
            Passed in an error message which is sent to error logger. Makes
            "file error" image clickable to be hidden (and also try reloading
            a board again)
        Parameters -- error_msg -- a string (str) describing the error in reading
            puzz file from loading function. Gets passed to error logger.
    '''
    global screen
    
    error_logger(error_msg)

    def dismiss_error_msg(x,y):
        '''
        Callback Function -- Called when clicking file_error image in Turtle dispaly.
            Makes the image hide and also calls loading board function again.
        '''
        return process_error.hideturtle(), load_new_board()
    
    screen.addshape("Resources/file_error.gif")
    process_error = turtle.Turtle()
    process_error.shape("Resources/file_error.gif")
    process_error.showturtle()

    process_error.onclick(dismiss_error_msg)


def error_logger(error : str):
    '''
    Helper Function -- takes in an error string from other functions,
            opens up an error file (creates it if doesn't exist yet)
            and appends error string to end of the file
        Parameters -- error -- a string (str) describing an issue from
            anotherfunction.
    '''
    print(error + "\n")
    with open("5001_puzzle.err", mode = "a") as error_file:
        error += "\n"
        error_file.write(error)
    print("Error Puzz File Updated\n")


def initial_setup():
    '''
    Helper/Driver Function -- Sets up the game after the splash screen.
        Gets the player name and move_limit inputs from player, draws the
        outlines on the Turtle screen, and gets the leaderboard
    '''

    global move_limit
    global player_name
    global score_to_beat
    global game_board

    player_name = ""
    try:
        while len(player_name) > 4 or len(player_name) == 0:
            player_name = screen.textinput("Welcome to CS5001 Puzzle Slider",
                                "Choose Your Player Tag [2-4 Characters]:")
    except TypeError:
        # Default to USER if player presses "Cancel"
        player_name = "USER"

    move_limit = 0

    try:
        while move_limit < LOWER_MOVE_BOUND or move_limit > UPPER_MOVE_BOUND: 
            move_limit = int(screen.textinput("CS5001 Puzzle Slider - Moves",
                      "Enter the # of moves allowed [5-200 or default 10] "))
    except TypeError:
        
        # Default of 10 if player presses "Cancel"
        move_limit = 10

    except ValueError:
        # Default of 10 if Player doesn't enter a valid integer
        move_limit = 10
        
    # Draw play area outlines
    draw_outlines(-450, 450, 10, "black", 550, 700)

    # Draw status area (reset/load/quit buttons)
    draw_outlines(-450, -315, 10, "black", 875, 115)

    # Draw leaderboard area
    draw_outlines(125, 450, 6, "blue", 300, 700)
    create_status_buttons()

    # Setup board
    game_board = Board("mario.puz", move_limit)

    # Fetch leaderboard data
    leaderboard = get_leaderboard()
    if leaderboard:
        sorted_lb = sort_leaderboard(leaderboard)
        score_to_beat = sorted_lb[0][0]
        display_leaderboard(sorted_lb)
    else:
        score_to_beat = UPPER_MOVE_BOUND

    
def main():
    # Screen Setup
    global screen

    screen = turtle.Screen()
        
    screen.setup(SCREEN_HEIGHT, SCREEN_WIDTH)
    screen.title("CS 5001 Sliding Puzzle Game")

    screen.addshape("Resources/splash_screen.gif")

    splash = turtle.Turtle()
    splash.shape("Resources/splash_screen.gif")

    screen.ontimer(splash.hideturtle, t=SPLASH_TIMER)
    screen.ontimer(initial_setup, t= SPLASH_TIMER)

    
if __name__ == "__main__":
    main()
turtle.done()
