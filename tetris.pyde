import random

BOARD_WIDTH = 200
BOARD_HEIGHT = 400
CELL_WIDTH = 20
CELL_HEIGHT = 20
NUM_ROWS = BOARD_HEIGHT/CELL_HEIGHT
NUM_COLS = BOARD_WIDTH/CELL_WIDTH
COLORS = [[255, 51, 52], [12, 150, 228], [30, 183, 66], [246, 187, 0], [255, 255, 255], [0, 0, 0]]


class Block:
    def __init__(self):
        self.w = CELL_WIDTH
        self.h = CELL_HEIGHT
        self.c = random.randint(0, 5)
        self.x = self.bpositionx()
        self.y = 0
    
    def fill_color(self):
        return fill(COLORS[self.c][0], COLORS[self.c][1], COLORS[self.c][2])
        
    def bpositionx(self):
        #assign a random position for a block upon creation
        x = random.randint(0, NUM_COLS-1)
        return (x*self.w)
    
    def display(self):
        self.fill_color()
        rect(self.x, self.y, self.w, self.h)    
            
class Game:
    def __init__(self):
        self.score = 0
        self.speed = 0
        self.board = [] #2d list storing either empty space or the integer value of the block color (0-5) in each cell
        self.blocks = [] #list of all blocks on the board
        for r in range(NUM_ROWS):
            r_list = []
            for c in range(NUM_COLS):
                r_list.append(" ")
            self.board.append(r_list)
        
        self.new_block()
    
    def display(self):
        if not self.over():
            self.set_up() 
        
            if keyPressed:
                #user can use either a, d or <-, -> to move blocks
                if (key == 'a' or keyCode == LEFT) and self.right_empty():
                    self.current_block.x -= CELL_WIDTH
                elif (key == 'd' or keyCode == RIGHT) and self.left_empty():
                    self.current_block.x += CELL_WIDTH
            
            #move currently selected block down until it reaches the bottom or another block below        
            if self.current_block.y<(BOARD_HEIGHT-CELL_HEIGHT) and self.board[self.current_block.y/CELL_HEIGHT+1][self.current_block.x/CELL_WIDTH] == " ":
                self.current_block.y += CELL_HEIGHT
        
            else:
                #change corresponding cell in the board 2d list to block color
                self.board[self.current_block.y/CELL_HEIGHT][self.current_block.x/CELL_WIDTH] = self.current_block.c
                if self.isfour():
                    #increase score and reset speed if 
                    self.score += 1
                    self.speed = 0
                else:
                    self.speed += 0.25
                self.new_block()
                
            for x in self.blocks:
                x.display()
            
            #display the score
            fill(0)
            textSize(15)
            text("Score: " + str(self.score), BOARD_WIDTH-75, 19)
            
        else:
            #inform the user of the end of the game and further actions   
            fill(0)
            textSize(20)
            text("GAME OVER :(", BOARD_WIDTH/5, BOARD_HEIGHT/2-3)
            textSize(15)
            text("Score: " + str(self.score), BOARD_WIDTH/3, BOARD_HEIGHT/2+25)
            textSize(10)
            text("Click to restart", BOARD_WIDTH/3, BOARD_HEIGHT/2+50)
            
    def new_block(self):
        #create a new instance of Block and append it to the list of blocks
        self.current_block = Block()
        while self.board[self.current_block.y/CELL_HEIGHT][self.current_block.x/CELL_WIDTH] != " ":
            self.current_block = Block()
        self.blocks.append(self.current_block)
        
    def remove_block(self, x, y):
        #search for a block with matchin coordinates(x,y) in the list of blocks and remove it
        for block in self.blocks:
            if block.x == x and block.y == y:
                self.blocks.remove(block)
    
    def isfour(self):
        #method to check if four blocks of the same color are alligned vertically
        isfour = False
        try:
            for x in range(1, 4):
                if self.board[self.current_block.y/CELL_HEIGHT + x][self.current_block.x/CELL_WIDTH] == self.current_block.c:
                    isfour = True
                else:
                    return False
        except IndexError:
            return False
        
        if isfour:
            #remove 4 alligned blocks
            for x in range(0, 4):
                self.board[self.current_block.y/CELL_HEIGHT + x][self.current_block.x/CELL_WIDTH] = " "
                self.remove_block(self.current_block.x, self.current_block.y + x*CELL_HEIGHT)
        
        return isfour
    
    def over(self):
        #method to check if the board is full
        if len(self.blocks) == NUM_ROWS*NUM_COLS:
            return True
        return False
                
    def set_up(self):
        #show the board with lines before showing blocks
        background(210)
        stroke(180)
        for x in range(NUM_ROWS):
            line(0, CELL_WIDTH*x, BOARD_WIDTH, CELL_WIDTH*x)
        for x in range(NUM_COLS):
            line(CELL_HEIGHT*x, 0, CELL_HEIGHT*x, BOARD_HEIGHT)
    
    def left_empty(self):
        #method to check if a cell to the left exists and is empty
        try:
            if self.current_block.x<(BOARD_WIDTH-CELL_WIDTH) and self.board[self.current_block.y/CELL_HEIGHT][self.current_block.x/CELL_WIDTH+1] == " ":
                return True
            return False
        except:
            return False
    
    def right_empty(self):
        #method to check if a cell to the right exists and is emppty
        try:
            if self.current_block.x>0 and self.board[self.current_block.y/CELL_HEIGHT][self.current_block.x/CELL_WIDTH-1] == " ":
                return True
            return False
        except:
            return False
        
            
        

game = Game()

def setup():
    size(BOARD_WIDTH, BOARD_HEIGHT)

def draw():
    if frameCount%(max(1, int(8-game.speed)))==0 or frameCount==1:
        game.display()

def mouseClicked():
    #if mouse is clicked after the game is over, reset the game
    if game.over():
        game.__init__()
