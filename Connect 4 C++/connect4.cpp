#include <iostream>
using namespace std;

/* Program name: c4-code.cpp
   Purpose: Recreates the game connect 4, which involves two players 
dropping discs of two colors into slots of the game-board, hoping to make a pattern of four discs of the same color (either horizontally, vertically, or diagonally)
   Created & Modified by: Bryan Dumond
   Date of completion: 11/27/12
*/

const int ROWS = 7, COLUMNS = 7;

struct Cell {
	bool is_empty;
	char chip;
	int colnum;
	};

void initialize (Cell board[][COLUMNS], int column_chips[COLUMNS]);
void run_game (Cell board[][COLUMNS], int column_chips[COLUMNS]);
void draw_board (Cell board[][COLUMNS]);
int get_input (int column_chips[COLUMNS], int turnnum);
bool check_input (int column_chips[COLUMNS], int input);
int insert_chip (Cell board[][COLUMNS], int column_chips[COLUMNS],
		 int turnnum, int input);
char check_turn (int turnnum);
bool check_tie (int column_chips[COLUMNS]);
bool check_win (Cell board[][COLUMNS], int turnnum);
bool check_diag (Cell board[][COLUMNS]);
bool upward_right (Cell board[][COLUMNS]);
bool upward_left (Cell board[][COLUMNS]);
bool check_horiz (Cell board[][COLUMNS]);
bool check_vert (Cell board[][COLUMNS]);

//This is the function which creates the connect 4 board and the 1D
//array that will keep track of how many chips are in each column.
//I refer to each individual "space" where a chip can land as a "cell"

int main()
{
	Cell	board[ROWS][COLUMNS];
	int column_chips[COLUMNS];
	initialize (board, column_chips);
	run_game (board, column_chips);
}

//This function is called by main and initializes the game board and the
//1D array created by main. It makes all cells empty and the 1D array's
//elements all equal to zero

void initialize (Cell board[][COLUMNS], int column_chips[COLUMNS])
{
	int pos = 0, rpos = 0, cpos = 0;

	while (rpos < ROWS)
	{
		while (cpos < COLUMNS)
		{
			board[rpos][cpos].chip = ' ';
			board[rpos][cpos].is_empty = true;
			board[rpos][cpos].colnum = cpos+1;
			cpos++;
		}
		cpos = 0;
		rpos++;
	}
	while (pos < COLUMNS)
	{
		column_chips[pos] = 0;
		pos++;
	}
}

// The main loop that keeps the program from quitting until someone 
// either wins the game or there is a draw. It does no calculations itself,
// it just calls other functions for those. After a draw or after somebody
// wins, the board is displayed one last time to the user to show the final
// results, and then the program closes. 

void run_game (Cell board[][COLUMNS], int column_chips[COLUMNS])
{
	int turnnum = 0, input;
	bool win = false, tie = false;
	
	while (win == false && tie == false)
	{
		draw_board (board);
		input = get_input (column_chips, turnnum);
		turnnum = insert_chip (board, column_chips,turnnum,
			  	       input);
		win = check_win (board, turnnum);
		tie = check_tie (column_chips);
	}
	draw_board (board);
}

// Function that draws the board. This function is a void function and 
// therefore doesn't return anything; it just modifies the 2D array that
// is the connect 4 board and draws it.

void draw_board (Cell board[][COLUMNS]){
	int topsidecount = 0, rpos = 0, cpos = 0, rowcount = 0;

	while (rowcount < ROWS - 1){
		while (topsidecount < COLUMNS){
			cout << "+---";
			topsidecount++;
		}
		cout << "+" << endl;
		topsidecount = 0;
		while (topsidecount < COLUMNS){
			cout << "| " << board[rpos][cpos].chip << " ";
			topsidecount++;
			cpos++;
		}
		cout << "|" << endl;
		topsidecount = 0;
		cpos = 0;
		rowcount++;
		rpos++;
	}
	while (topsidecount < COLUMNS){
		cout << "+---";
		topsidecount++;
	}
	cout << "+" << endl;
	topsidecount = 0, rpos = 0, cpos = 0;
	while (topsidecount < COLUMNS){
		cout << "| " << board[rpos][cpos].colnum << " ";
		topsidecount++;
		cpos++;
	}
	cout << "|" << endl;
	topsidecount = 0;
	while (topsidecount < COLUMNS){
		cout << "+---";
		topsidecount++;
	}
	cout << "+" << endl;
}

// This function is what controls user input. It determines whose
// turn it is and requests that this player make a move. It then calls
// another function to process that input (see if it is valid) and then
// returns the first valid input to run_game so that it can be used to 
// fill in the connect 4 board.

int get_input (int column_chips[COLUMNS], int turnnum)
{
	int player, divisor = 2, input = 0, goodinput = 0;
	bool invalid = true;

	player = turnnum%divisor;
	while (invalid == true)
	{
		if (player == 0)
		{
			cout << "Player 1, make your move!" << endl;
		}
		if (player == 1)
		{
			cout << "Player 2, make your move!" << endl;
		}
		cin >> input;
		invalid = check_input (column_chips,input);
	}
	if (invalid == false)
	{
		goodinput = input;
	}
	return goodinput;
}
// This is the function called by get_input that checks whether or 
// not the user's input is valid. User is only allowed to enter a number
// between 1 and 7. Non-integers will automatically have their decimal 
// parts removed and just the whole number part will be used. The function
// also checks that there are enough free spaces in teh column the user
// wants to modify.

bool check_input (int column_chips[COLUMNS], int input)
{
	bool check;
	if ((input >= 1 && input <= COLUMNS) && (column_chips[input-1]
	     < (ROWS - 1)))
	{
		check = false;
	}
	else
	{
		check = true;
	}
	return check;
}

// This is the function that actually edits the connect 4 board and
// inserts the chip. It receives the valid input from run_game and 
// also the number of turns that have happened in the game thus far.
// It uses this number to determine whether to insert a yellow or a
// red chip into the board. It also updates the turn count and returns
// it to run_game so that it can be used for other functions.

int insert_chip (Cell board[][COLUMNS], int column_chips[COLUMNS],
		 int turnnum, int input)
{
	int rpos;
	char color;
	bool chip_inserted;
	
	rpos = 5;
	chip_inserted = false;
	color = check_turn (turnnum);
	while (chip_inserted == false)
	{
		while ((board[rpos][input-1].is_empty == false)&&(rpos >= 0))
		{
			rpos--;
		}
		if (board[rpos][input-1].is_empty == true)
		{
			board[rpos][input-1].is_empty = false;
			board[rpos][input-1].chip = color;
			column_chips[input-1]++;
			chip_inserted = true;
		}
	}
	turnnum++;
	return turnnum;	
}

// This is the function that insert chip calls to determine whether to insert
// a red chip or a yellow chip, depending on whose turn it is.

char check_turn (int turnnum)
{
	char color;
	int decision;

	decision = turnnum%2;
	if (decision == 0)
	{
		color = 'R'; //@@ const char P1 = 'R' would have been nice
	}
	else
	{
		color = 'Y';
	}
	return color;
}

// This is the function that checks for a tie in the game by checking
// whether all of the columns are full (by analyzing the 1D array that 
// tracks how many chips are in each column).

bool check_tie (int column_chips[COLUMNS])
{
	int pos = 0, fullcolcount = 0;
	bool decision;

	while (pos < COLUMNS)
	{
		if (column_chips[pos]== ROWS-1)
		{
			fullcolcount++;
		}
		pos++;
	}
	if (fullcolcount == COLUMNS)
	{
		decision = true;
		cout << "DRAW" << endl;
	}
	if (fullcolcount != COLUMNS)
	{
		decision = false;
	}	
	return decision;
}	

// This is the function that checks whether a player has won. It does
// so by calling multiple functions which will chech for a horizontal,
// vertical, or diagonal victory. A victory is defined as any four 
// chips which form a continuous line (horizontal, vertical, or diagonal)
// on the board.

bool check_win (Cell board[][COLUMNS], int turnnum)
{
	bool diagwin, horizwin, vertwin, win;
	int turnnumtemp, winner;
	
	
	horizwin = check_horiz (board);
	vertwin = check_vert (board);
	diagwin = check_diag (board);
	if (horizwin == true || vertwin == true || diagwin == true)
	{
		win = true;
		turnnumtemp = turnnum - 1;
		winner = turnnumtemp%2;
		if (winner == 0)
		{
			cout << "PLAYER 1 WINS" << endl;
		}
		if (winner == 1)
		{
			cout << "PLAYER 2 WINS" << endl;
		}
	}
	else
	{
		win = false;
	}
	return win;
}

// This function checks for a diagonal victory; either up-left diagonal
// or up-right diagonal. These two types of victories are checked for by
// two separate functions (named respectively for their direction). A 
// victory consists of 4 chips of the same color forming a continuous
// diagonal line on the board.

bool check_diag (Cell board[][COLUMNS])
{
	bool upleft, upright, diagwin;

	upleft = upward_left (board);
	upright = upward_right (board);

	if (upleft == true || upright == true)
	{
		diagwin = true;
	}
	else
	{
		diagwin = false;
	}
	return diagwin;
}

// This is the function that checks for a diagonal victory that goes
// upward and to the right. The four chips must be of the same color
// for a victory.

bool upward_right (Cell board[][COLUMNS])
{
//@@ diag_right_check would have been a better name
	int rpos, cpos, chipcount, chiprpos, chipcpos;
	bool win;
	char chipcolor;

	rpos = 5;
	cpos = 0;
	chipcount = 0;
	while (rpos >= 3 && chipcount < 4)
	{
		while (cpos <= 3 && chipcount < 4)
		{
			chipcount = 0;
			if (board[rpos][cpos].is_empty == false)
			{
				chipcolor = board[rpos][cpos].chip;
				chipcount++;
				chipcpos = cpos + 1;
				chiprpos = rpos - 1;
				while (board[chiprpos][chipcpos].chip
				       == chipcolor && chipcount < 4)
				{
					chipcount++;
					chipcpos++;
					chiprpos--;
				}
			}
			cpos++;	
		}
		cpos = 0;
		rpos--;
	}
	if (chipcount == 4)
	{
		win = true;
	}
	else {
		win = false;
	}
	return win;
}

// This function checks for a diagonal victory that goes upwards and to 
// the left. The four chips must be of the same color for a victory.

bool upward_left (Cell board[][COLUMNS])
{
//@@ diag_left_check would have been clearer here
	int rpos, cpos, chipcount, chiprpos, chipcpos;
	bool win;
	char chipcolor;

	rpos = 5;
	cpos = 3;
	chipcount = 0;
	while (rpos >= 3 && chipcount < 4)
	{
		while (cpos < COLUMNS && chipcount < 4)
		{
			chipcount = 0;
			if (board[rpos][cpos].is_empty == false)
			{
				chipcolor = board[rpos][cpos].chip;
				chipcount++;
				chipcpos = cpos - 1;
				chiprpos = rpos - 1;
				while (board[chiprpos][chipcpos].chip
				       == chipcolor && chipcount < 4)
				{
					chipcount++;
					chipcpos--;
					chiprpos--;
				}
			}
			cpos++;	
		}
		cpos = 3;
		rpos--;
	}
	if (chipcount == 4)
	{
		win = true;
	}
	else {
		win = false;
	}
	return win;	
}

// This function checks for a horizontal line victory of four chips of 
// the same color are lined up right next to each other

bool check_horiz (Cell board[][COLUMNS])
{
	int rpos, cpos, chipcount, chipcpos;
	bool win;
	char chipcolor;
	
	rpos = 5;
	cpos = 0;
	chipcount = 0;
	while (rpos > 0 && chipcount < 4)
	{
		while (cpos <= 3 && chipcount < 4)
		{
			chipcount = 0;
			if (board[rpos][cpos].is_empty == false)
			{
				chipcolor = board[rpos][cpos].chip;
				chipcount++;
				chipcpos = cpos + 1;
				while (board[rpos][chipcpos].chip == chipcolor
					&& chipcount < 4)
				{
					chipcount++;
					chipcpos++;
				}
			}
			cpos++;	
		}
		cpos = 0;
		rpos--;
	}
	if (chipcount == 4)
	{
		win = true;
	}
	else {
		win = false;
	}
	return win;
}

// This function checks for a vertical line victory, where four chips of 
// the same color are stacked on top of each other.

bool check_vert (Cell board[][COLUMNS]) 
{
	int rpos,cpos, chipcount, chiprpos;
	bool win;
	char chipcolor;
	
	rpos = 5;
	cpos = 0;
	chipcount = 0;
	while (rpos >= 3 && chipcount < 4)
	{
		while (cpos <= COLUMNS && chipcount < 4)
		{
			chipcount = 0;
			if (board[rpos][cpos].is_empty == false)
			{
				chipcolor = board[rpos][cpos].chip;
				chipcount++;
				chiprpos = rpos - 1;
				while (board[chiprpos][cpos].chip == chipcolor
					&& chipcount < 4)
				{
					chipcount++;
					chiprpos--;
				}
			}
			cpos++;	
		}
		cpos = 0;
		rpos--;
	}
	if (chipcount == 4)
	{
		win = true;
	}
	else {
		win = false;
	}
	return win;
}
